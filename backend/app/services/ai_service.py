from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from app.config import settings
from app.schemas.plan import WeeklyPlanAI, UserProfileData
import logging

logger = logging.getLogger(__name__)

class AIWorkoutPlanner:
    """Service for generating workout plans using AI"""

    def __init__(self):
        self.llm = ChatOpenAI(
            model="gpt-4-turbo-preview",
            temperature=0.7,
            openai_api_key=settings.OPENAI_API_KEY
        )
        self.structured_llm = self.llm.with_structured_output(WeeklyPlanAI)

    async def generate_plan(self, user_data: UserProfileData) -> WeeklyPlanAI:
        """Generate a personalized 7-day workout plan"""
        
        prompt_template = """
        Ты - экспертный фитнес-тренер, специализирующийся на тренировках с собственным весом, которые можно отслеживать с помощью компьютерного зрения.
        Твоя задача - создать персонализированный план тренировок на 7 дней для пользователя со следующими параметрами:
        - Возраст: {age} лет
        - Вес: {weight} кг
        - Рост: {height} см
        - Цель: {goal}
        - Уровень: {level}
        
        ВАЖНЫЕ ОГРАНИЧЕНИЯ:
        1. Используй ТОЛЬКО эти типы упражнений: "Приседания", "Выпады", "Отжимания", "Планка". Это связано с тем, что наше приложение отслеживает только их через камеру.
        2. План должен быть на 7 дней.
        3. Для "Планка" указывай `duration` (секунды) и `reps=None`.
        4. Для остальных упражнений указывай `reps` и `duration=None`.
        5. Объясняй инструкции к упражнениям на РУССКОМ языке.
        6. Сделай план прогрессивным и мотивирующим.
        """

        prompt = ChatPromptTemplate.from_template(prompt_template)
        
        # Mapping goals and levels to Russian for better context if they are in English
        goal_map = {
            "lose_weight": "Похудение",
            "get_toned": "Приведение мышц в тонус",
            "improve_shape": "Улучшение общей физической формы"
        }
        level_map = {
            "beginner": "Новичок",
            "intermediate": "Средний",
            "advanced": "Продвинутый"
        }

        formatted_goal = goal_map.get(user_data.fitness_goal, user_data.fitness_goal)
        formatted_level = level_map.get(user_data.fitness_level, user_data.fitness_level)

        try:
            return await self.structured_llm.ainvoke(
                prompt.format(
                    age=user_data.age,
                    weight=user_data.weight,
                    height=user_data.height,
                    goal=formatted_goal,
                    level=formatted_level
                )
            )
        except Exception as e:
            logger.error(f"AI Plan Generation failed: {e}")
            # Fallback to a basic plan or raise
            raise e

ai_planner = AIWorkoutPlanner()
