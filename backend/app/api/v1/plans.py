from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, update
from datetime import date, timedelta
from app.database import get_db
from app.api.deps import get_current_user
from app.models.user import User, UserProfile
from app.models.plan import WorkoutPlan, PlanDay, PlannedExercise
from app.services.ai_service import ai_planner
from app.schemas.plan import UserProfileData
import logging

logger = logging.getLogger(__name__)
router = APIRouter()

@router.post("/generate")
async def generate_monthly_plan(
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Generate a new 30-day monthly plan using AI based on user profile"""
    
    # Get user profile
    result = await db.execute(
        select(UserProfile).filter(UserProfile.user_id == current_user.id)
    )
    profile = result.scalars().first()
    
    if not profile or not profile.age:
        raise HTTPException(status_code=400, detail="User profile is incomplete")
    
    user_data = UserProfileData(
        age=profile.age,
        weight=profile.weight,
        height=profile.height,
        fitness_goal=profile.fitness_goal,
        fitness_level=profile.fitness_level
    )
    
    # Generate 30-day plan via AI
    logger.info(f"Generating 30-day plan for user {current_user.id}")
    ai_plan = await ai_planner.generate_plan(user_data)

    # Deactivate old plans
    await db.execute(
        update(WorkoutPlan)
        .filter(WorkoutPlan.user_id == current_user.id)
        .values(is_active=False)
    )

    # Create new WorkoutPlan
    new_plan = WorkoutPlan(
        user_id=current_user.id,
        week_start_date=date.today(),  # Actually plan_start_date
        is_active=True
    )
    db.add(new_plan)
    await db.flush() # Get plan.id
    
    # Create days and exercises (30 days instead of 7)
    for i, ai_day in enumerate(ai_plan.days):
        plan_day = PlanDay(
            plan_id=new_plan.id,
            day_number=ai_day.day_number - 1,  # Convert 1-30 to 0-29 for storage
            date=date.today() + timedelta(days=i),
            is_rest_day=ai_day.is_rest_day
        )
        db.add(plan_day)
        await db.flush()
        
        for idx, ai_ex in enumerate(ai_day.exercises):
            # Map Russian names back to internal values if needed, 
            # but let's assume ExerciseType enum handles strings or we match carefully
            ex_type_map = {
                "Приседания": "squat",
                "Выпады": "lunge",
                "Отжимания": "pushup",
                "Планка": "plank"
            }
            internal_type = ex_type_map.get(ai_ex.exercise_type, ai_ex.exercise_type.lower())
            
            planned_ex = PlannedExercise(
                plan_day_id=plan_day.id,
                exercise_type=internal_type,
                target_sets=ai_ex.sets,
                target_reps=ai_ex.reps if ai_ex.reps else (ai_ex.duration if ai_ex.duration else 0),
                estimated_minutes=5, # Simplified
                order_index=idx
            )
            db.add(planned_ex)
            
    await db.commit()
    logger.info(f"Successfully created 30-day plan {new_plan.id} for user {current_user.id}")
    return {
        "status": "success",
        "plan_id": str(new_plan.id),
        "duration_days": len(ai_plan.days)
    }

@router.get("/current")
async def get_current_plan(
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Get the active workout plan for the current user"""
    result = await db.execute(
        select(WorkoutPlan)
        .filter(WorkoutPlan.user_id == current_user.id, WorkoutPlan.is_active == True)
    )
    plan = result.scalars().first()
    
    if not plan:
        raise HTTPException(status_code=404, detail="No active plan found")
        
    # In a real response we would use a proper Pydantic schema with nested data
    # For now, let's return a simple structure or the plan object if SQLAlchemy allows
    return plan
