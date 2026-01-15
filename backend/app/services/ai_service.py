from langchain_openai import AzureChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from app.config import settings
from app.schemas.plan import MonthlyPlanAI, UserProfileData
import logging

logger = logging.getLogger(__name__)

class AIWorkoutPlanner:
    """Service for generating workout plans using AI"""

    def __init__(self):
        self.llm = AzureChatOpenAI(
            azure_endpoint=settings.AZURE_OPENAI_ENDPOINT,
            openai_api_key=settings.AZURE_OPENAI_API_KEY,
            deployment_name=settings.AZURE_OPENAI_DEPLOYMENT,
            openai_api_version=settings.AZURE_OPENAI_API_VERSION,
            temperature=0.7
        )
        self.structured_llm = self.llm.with_structured_output(MonthlyPlanAI)

    def _calculate_age_modifier(self, age: int) -> float:
        """Calculate volume scaling factor based on age (for reference, AI decides)"""
        if age < 20:
            return 0.85
        elif 20 <= age < 40:
            return 1.0
        elif 40 <= age < 60:
            return 0.80
        else:
            return 0.60

    def _generate_prompt_variables(self, user_data: UserProfileData) -> dict:
        """Generate dynamic prompt variables based on user profile"""

        # Mapping to Russian
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

        # Calculate rest days based on age
        rest_days_count = 10 if user_data.age >= 60 else 8

        return {
            "age": user_data.age,
            "weight": user_data.weight,
            "height": user_data.height,
            "goal": goal_map.get(user_data.fitness_goal, user_data.fitness_goal),
            "level": level_map.get(user_data.fitness_level, user_data.fitness_level),
            "rest_days_count": rest_days_count
        }

    async def generate_plan(self, user_data: UserProfileData) -> MonthlyPlanAI:
        """Generate a personalized 30-day workout plan with intelligent progression"""

        prompt_template = """
Ты - экспертный фитнес-тренер, специализирующийся на научно обоснованной прогрессии тренировок с собственным весом.
Твоя задача - создать персонализированный 30-дневный план тренировок с прогрессивной перегрузкой.

ПРОФИЛЬ ПОЛЬЗОВАТЕЛЯ:
- Возраст: {age} лет
- Вес: {weight} кг
- Рост: {height} см
- Цель: {goal}
- Уровень: {level}

КРИТИЧЕСКИ ВАЖНЫЕ ОГРАНИЧЕНИЯ:
1. Используй ТОЛЬКО эти 4 упражнения (ограничение компьютерного зрения):
   - "Приседания" (для ног и ягодиц)
   - "Выпады" (для ног и баланса)
   - "Отжимания" (для груди, плеч, трицепсов)
   - "Планка" (для кора и стабилизации)

2. План должен быть РОВНО на 30 дней (days list должен содержать 30 элементов).

3. Дни отдыха:
   - {rest_days_count} дней отдыха из 30 дней
   - Распределены по схеме: 3 дня тренировок, 1 день отдыха
   - Для дней отдыха: is_rest_day=True, exercises=[]

4. Прогрессивная перегрузка по неделям:

   НЕДЕЛЯ 1 (дни 1-7) - ОСНОВАНИЕ:
   Фокус: техника выполнения, привыкание к нагрузке, базовые объемы
   Адаптируй сложность под возраст и уровень пользователя

   НЕДЕЛЯ 2 (дни 8-14) - НАРАЩИВАНИЕ ОБЪЕМА:
   Увеличь повторения на 10-20% по сравнению с неделей 1
   Фокус: увеличение работоспособности

   НЕДЕЛЯ 3 (дни 15-21) - ПИК ИНТЕНСИВНОСТИ:
   Добавь подходы или увеличь интенсивность
   Фокус: пиковая нагрузка, максимальная адаптация

   НЕДЕЛЯ 4 (дни 22-30) - КОНСОЛИДАЦИЯ:
   Поддержание объема с небольшим снижением для восстановления
   Фокус: закрепление результатов, подготовка к следующему циклу

5. Учитывай цель пользователя:
   - Похудение: больше повторений (15-20+), короткий отдых между подходами, круговая тренировка
   - Тонус: умеренные объемы (12-15 повторений), сбалансированный подход
   - Форма: варьируй нагрузку, микс силы и выносливости

6. Учитывай возраст пользователя:
   - Молодые (<30): стандартная прогрессия
   - Средний возраст (30-50): осторожная прогрессия, больше внимания восстановлению
   - Старшие (50+): щадящие объемы, больше дней отдыха, акцент на технику

7. Количество упражнений в день:
   - Новичок: 2-3 упражнения
   - Средний: 3-4 упражнения
   - Продвинутый: 4 упражнения
   Чередуй акценты: день 1 - ноги, день 2 - верх тела, день 3 - комплексная тренировка

ВАЖНО ДЛЯ НОВИЧКОВ: Начинай ОЧЕНЬ легко (2 подхода × 8 повторений или даже меньше), чтобы не перегрузить пользователя.
Лучше начать слишком легко, чем слишком тяжело. Пользователь должен закончить первую неделю с чувством "я могу больше", а не "я еле выжил".
Это критически важно для мотивации и предотвращения травм.

ТЕХНИЧЕСКИЕ ТРЕБОВАНИЯ:
- Для "Планка": указывай duration (секунды) и reps=None
- Для остальных упражнений: указывай sets, reps и duration=None
- instructions: краткое описание техники и фокуса на русском языке (1-2 предложения)
- daily_focus: тема дня на русском ("Ноги и ягодицы", "Верх тела", "Кор и стабилизация", "Полное тело", "День восстановления")
- day_number: от 1 до 30 (не от 0!)

ПРИМЕР СТРУКТУРЫ ДНЯ ТРЕНИРОВКИ:
{{
  "day_number": 1,
  "is_rest_day": false,
  "exercises": [
    {{
      "exercise_type": "Приседания",
      "sets": 2,
      "reps": 8,
      "duration": null,
      "instructions": "Опускайтесь до параллели бедра с полом, следите за тем, чтобы колени были над стопами. Держите спину прямой."
    }},
    {{
      "exercise_type": "Отжимания",
      "sets": 2,
      "reps": 6,
      "duration": null,
      "instructions": "Держите тело прямым от головы до пят, опускайтесь до угла 90° в локтях. Можно выполнять с колен для новичков."
    }},
    {{
      "exercise_type": "Планка",
      "sets": 2,
      "reps": null,
      "duration": 20,
      "instructions": "Держите прямую линию от головы до пяток, напрягите пресс и ягодицы. Не провисайте в пояснице."
    }}
  ],
  "daily_focus": "Вводная тренировка - основы техники"
}}

ПРИМЕР ДНЯ ОТДЫХА:
{{
  "day_number": 4,
  "is_rest_day": true,
  "exercises": [],
  "daily_focus": "День восстановления"
}}

Создай мотивирующий, научно обоснованный план с плавной прогрессией.
Пользователь должен чувствовать прогресс каждую неделю, но не должен быть перегружен.
Качество выполнения важнее количества повторений, особенно в первые недели.
        """

        prompt = ChatPromptTemplate.from_template(prompt_template)
        variables = self._generate_prompt_variables(user_data)

        try:
            logger.info(f"Generating 30-day plan for user: age={user_data.age}, level={user_data.fitness_level}, goal={user_data.fitness_goal}")
            plan = await self.structured_llm.ainvoke(prompt.format(**variables))
            logger.info(f"Successfully generated 30-day plan with {len(plan.days)} days")
            return plan
        except Exception as e:
            logger.error(f"AI Plan Generation failed: {e}")
            raise e

ai_planner = AIWorkoutPlanner()
