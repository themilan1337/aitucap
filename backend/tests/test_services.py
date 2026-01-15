
import pytest
from app.services.calories_service import calculate_exercise_calories, calculate_workout_calories
from app.services.achievement_service import ACHIEVEMENTS
from app.schemas.plan import UserProfileData

def test_calculate_calories():
    # Squat: MET 5.0, Weight 70kg, 60s (1 min), 10 reps
    # 5.0 * 70 * (60/3600) = 5.83
    # Bonus: 10 * 0.05 * 70 / 100 = 0.35
    # Total: 6.18
    cals = calculate_exercise_calories("squat", 60, 70, 10)
    assert cals == 6.18

    # Plank: MET 4.0, Weight 70kg, 60s, 0 reps
    # 4.0 * 70 * (60/3600) = 4.67
    # Total: 4.67
    cals = calculate_exercise_calories("plank", 60, 70, 0)
    assert cals == 4.67

def test_achievement_definitions():
    assert "first_workout" in ACHIEVEMENTS
    assert "streak_7" in ACHIEVEMENTS
    
    first_workout = ACHIEVEMENTS["first_workout"]
    assert first_workout["check"]({"total_workouts": 1}) == True
    assert first_workout["check"]({"total_workouts": 0}) == False

def test_user_profile_schema():
    profile = UserProfileData(
        age=25,
        weight=75.0,
        height=180,
        fitness_goal="lose_weight",
        fitness_level="beginner"
    )
    assert profile.age == 25
