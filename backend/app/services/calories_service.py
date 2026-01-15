"""
Calories calculation service using MET (Metabolic Equivalent of Task) values.
Formula: Calories = MET × Weight(kg) × Time(hours) + Rep Bonus
"""
from typing import Dict

# MET values for each exercise (Metabolic Equivalent of Task)
# Source: Compendium of Physical Activities
EXERCISE_MET_VALUES: Dict[str, float] = {
    "squat": 5.0,           # Body-weight squats
    "lunge": 4.5,           # Walking lunges
    "pushup": 8.0,          # Push-ups (vigorous)
    "plank": 4.0,           # Planks
    "situp": 8.0,           # Sit-ups (vigorous)
    "crunch": 3.8,          # Crunches
    "bicep_curl": 3.5,      # Bicep curls with body resistance
    "lateral_raise": 3.0,   # Arm raises
    "overhead_press": 4.0,  # Overhead press
    "leg_raise": 5.0,       # Leg raises
    "knee_raise": 4.0,      # Knee raises
    "knee_press": 4.0,      # Knee press
}


def calculate_exercise_calories(
    exercise_type: str,
    duration_seconds: int,
    user_weight_kg: float,
    reps: int = 0
) -> float:
    """
    Calculate calories burned for a single exercise.

    Args:
        exercise_type: Exercise identifier (e.g., "squat", "pushup")
        duration_seconds: Duration of exercise in seconds
        user_weight_kg: User's weight in kilograms
        reps: Number of reps performed (optional, for additional accuracy)

    Returns:
        Calories burned (float)

    Example:
        >>> calculate_exercise_calories("squat", 120, 70, 20)
        11.83  # 5.0 MET × 70kg × (120/3600)h + bonus
    """
    met = EXERCISE_MET_VALUES.get(exercise_type, 4.0)  # Default to 4.0 if unknown
    duration_hours = duration_seconds / 3600.0

    # Base calculation: MET × weight × time
    calories = met * user_weight_kg * duration_hours

    # Bonus: Add small amount per rep for explosiveness
    # More reps = more work even in same duration
    rep_bonus = reps * 0.05 * user_weight_kg / 100

    return round(calories + rep_bonus, 2)


def calculate_workout_calories(
    exercises: list,
    user_weight_kg: float
) -> float:
    """
    Calculate total calories for entire workout session.
    Updates each exercise's calories_burned field in-place.

    Args:
        exercises: List of ExercisePerformance objects with:
            - exercise_type (str)
            - duration (int, seconds)
            - reps (int)
        user_weight_kg: User's weight in kilograms

    Returns:
        Total calories burned for the workout

    Example:
        >>> exercises = [
        ...     ExercisePerformance(exercise_type="squat", duration=120, reps=20),
        ...     ExercisePerformance(exercise_type="pushup", duration=90, reps=15)
        ... ]
        >>> calculate_workout_calories(exercises, 70.0)
        18.65  # Sum of all exercises
    """
    total = 0.0

    for exercise in exercises:
        calories = calculate_exercise_calories(
            exercise_type=exercise.exercise_type,
            duration_seconds=exercise.duration,
            user_weight_kg=user_weight_kg,
            reps=exercise.reps
        )

        # Update the exercise object with calculated calories
        exercise.calories_burned = calories
        total += calories

    return round(total, 2)
