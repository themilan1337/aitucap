from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import datetime
from uuid import UUID

class ExercisePerformanceCreate(BaseModel):
    exercise_type: str
    reps: int
    duration: int # seconds
    form_accuracy: float # 0.0 - 1.0
    form_corrections: List[str] = []
    calories_burned: float
    order_index: int

class WorkoutSessionCreate(BaseModel):
    plan_day_id: Optional[UUID] = None
    started_at: datetime
    completed_at: datetime
    total_duration: int
    total_calories: float
    average_form_accuracy: float
    exercises: List[ExercisePerformanceCreate]

class ExercisePerformanceResponse(ExercisePerformanceCreate):
    id: UUID

    class Config:
        from_attributes = True

class WorkoutSessionResponse(BaseModel):
    id: UUID
    user_id: UUID
    plan_day_id: Optional[UUID]
    started_at: datetime
    completed_at: datetime
    total_duration: int
    total_calories: float
    average_form_accuracy: float
    exercises: List[ExercisePerformanceResponse]
    new_achievements: Optional[List[dict]] = None

    class Config:
        from_attributes = True
