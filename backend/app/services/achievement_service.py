"""
Achievement detection and awarding service.
Checks for milestone completions and unlocks badges.
"""
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func, desc
from datetime import datetime, timedelta, date
from app.models.achievement import UserAchievement
from app.models.workout import WorkoutSession
from typing import List, Dict
import logging

logger = logging.getLogger(__name__)

# Achievement definitions with check conditions
ACHIEVEMENTS = {
    "first_workout": {
        "name": "Первая тренировка",
        "description": "Выполните первую тренировку",
        "icon": "trophy",
        "check": lambda stats: stats["total_workouts"] >= 1
    },
    "workouts_10": {
        "name": "10 тренировок",
        "description": "Выполните 10 тренировок",
        "icon": "fire",
        "check": lambda stats: stats["total_workouts"] >= 10
    },
    "workouts_50": {
        "name": "50 тренировок",
        "description": "Выполните 50 тренировок",
        "icon": "star",
        "check": lambda stats: stats["total_workouts"] >= 50
    },
    "streak_7": {
        "name": "7-дневная серия",
        "description": "Тренируйтесь 7 дней подряд",
        "icon": "flame",
        "check": lambda stats: stats["current_streak"] >= 7
    },
    "perfect_form": {
        "name": "Идеальная форма",
        "description": "Достигните 95%+ точности",
        "icon": "medal",
        "check": lambda stats: stats["best_accuracy"] >= 95
    },
    "early_bird": {
        "name": "Ранняя пташка",
        "description": "Тренируйтесь до 8 утра",
        "icon": "sunrise",
        "check": lambda stats: stats["has_morning_workout"]
    }
}


async def calculate_user_stats(user_id: str, db: AsyncSession) -> Dict:
    """
    Calculate statistics needed for achievement checking.

    Args:
        user_id: User's UUID
        db: Database session

    Returns:
        Dictionary with user statistics:
        - total_workouts: Total number of completed workouts
        - current_streak: Current consecutive workout days
        - best_accuracy: Best form accuracy achieved
        - has_morning_workout: Whether user has worked out before 8am
    """

    # Total workouts
    result = await db.execute(
        select(func.count(WorkoutSession.id))
        .filter(WorkoutSession.user_id == user_id)
    )
    total_workouts = result.scalar() or 0

    # Best accuracy (convert to percentage 0-100)
    result = await db.execute(
        select(func.max(WorkoutSession.average_form_accuracy))
        .filter(WorkoutSession.user_id == user_id)
    )
    best_accuracy_raw = result.scalar() or 0
    best_accuracy = int(best_accuracy_raw * 100) if best_accuracy_raw else 0

    # Current streak
    current_streak = await calculate_streak(user_id, db)

    # Check for morning workout (before 8am)
    result = await db.execute(
        select(WorkoutSession)
        .filter(
            WorkoutSession.user_id == user_id,
            func.extract('hour', WorkoutSession.started_at) < 8
        )
        .limit(1)
    )
    has_morning_workout = result.scalars().first() is not None

    return {
        "total_workouts": total_workouts,
        "current_streak": current_streak,
        "best_accuracy": best_accuracy,
        "has_morning_workout": has_morning_workout
    }


async def calculate_streak(user_id: str, db: AsyncSession) -> int:
    """
    Calculate current workout streak (consecutive days with workouts).

    Args:
        user_id: User's UUID
        db: Database session

    Returns:
        Number of consecutive days with workouts

    Example:
        If user worked out on Dec 15, 14, 13, 12, 10 (skipped 11), streak = 4
    """

    # Get all workout dates (distinct days)
    result = await db.execute(
        select(func.date(WorkoutSession.completed_at).label('workout_date'))
        .filter(WorkoutSession.user_id == user_id)
        .distinct()
        .order_by(desc('workout_date'))
    )
    workout_dates = [row[0] for row in result.all()]

    if not workout_dates:
        return 0

    # Check if most recent workout was today or yesterday
    today = date.today()
    yesterday = today - timedelta(days=1)

    if workout_dates[0] not in [today, yesterday]:
        # Streak is broken (last workout was more than 1 day ago)
        return 0

    # Count consecutive days
    streak = 1
    expected_date = workout_dates[0] - timedelta(days=1)

    for workout_date in workout_dates[1:]:
        if workout_date == expected_date:
            streak += 1
            expected_date -= timedelta(days=1)
        else:
            # Gap found, streak ends
            break

    return streak


async def check_and_award_achievements(
    user_id: str,
    db: AsyncSession
) -> List[Dict]:
    """
    Check for new achievements and award them.

    Args:
        user_id: User's UUID
        db: Database session

    Returns:
        List of newly unlocked achievements with details:
        [{"type": "first_workout", "name": "...", "description": "...", "icon": "..."}]

    Example:
        >>> newly_unlocked = await check_and_award_achievements(user_id, db)
        >>> if newly_unlocked:
        ...     print(f"Unlocked: {newly_unlocked[0]['name']}")
    """

    # Calculate user stats
    stats = await calculate_user_stats(user_id, db)
    logger.debug(f"User {user_id} stats: {stats}")

    # Get already unlocked achievements
    result = await db.execute(
        select(UserAchievement.achievement_type)
        .filter(
            UserAchievement.user_id == user_id,
            UserAchievement.unlocked_at.isnot(None)
        )
    )
    unlocked_types = {row[0] for row in result.all()}

    # Check each achievement
    newly_unlocked = []

    for achievement_type, achievement_def in ACHIEVEMENTS.items():
        # Skip if already unlocked
        if achievement_type in unlocked_types:
            continue

        # Check if condition is met
        if achievement_def["check"](stats):
            # Award achievement
            new_achievement = UserAchievement(
                user_id=user_id,
                achievement_type=achievement_type,
                name=achievement_def["name"],
                description=achievement_def["description"],
                icon=achievement_def["icon"],
                unlocked_at=datetime.utcnow(),
                progress=100,
                target=100
            )
            db.add(new_achievement)

            newly_unlocked.append({
                "type": achievement_type,
                "name": achievement_def["name"],
                "description": achievement_def["description"],
                "icon": achievement_def["icon"]
            })

            logger.info(f"🏆 Achievement unlocked: {achievement_type} for user {user_id}")

    if newly_unlocked:
        await db.commit()
        logger.info(f"Total {len(newly_unlocked)} new achievements for user {user_id}")

    return newly_unlocked
