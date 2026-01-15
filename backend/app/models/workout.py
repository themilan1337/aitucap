from sqlalchemy import Column, String, Integer, Float, Boolean, DateTime, ForeignKey, JSON
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
import uuid

from app.database import Base


class WorkoutSession(Base):
    """Completed workout session"""

    __tablename__ = "workout_sessions"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    plan_day_id = Column(UUID(as_uuid=True), ForeignKey("plan_days.id", ondelete="SET NULL"), nullable=True)

    # Workout timing
    started_at = Column(DateTime(timezone=True), nullable=False)
    completed_at = Column(DateTime(timezone=True), nullable=False, index=True)

    # Aggregated stats
    total_duration = Column(Integer, nullable=False)  # seconds
    total_calories = Column(Float, nullable=False)
    average_form_accuracy = Column(Float, nullable=False)  # 0.0 - 1.0
    is_completed = Column(Boolean, default=True)

    # Relationships
    user = relationship("User", back_populates="workout_sessions")
    plan_day = relationship("PlanDay", back_populates="workout_sessions")
    exercises = relationship("ExercisePerformance", back_populates="workout_session", cascade="all, delete-orphan", order_by="ExercisePerformance.order_index")

    def __repr__(self):
        return f"<WorkoutSession(id={self.id}, user_id={self.user_id}, date={self.completed_at})>"


class ExercisePerformance(Base):
    """Individual exercise performance within a workout"""

    __tablename__ = "exercise_performances"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    workout_session_id = Column(UUID(as_uuid=True), ForeignKey("workout_sessions.id", ondelete="CASCADE"), nullable=False, index=True)
    exercise_type = Column(String(50), nullable=False)  # 'squat' | 'lunge' | 'pushup' | 'plank'
    reps = Column(Integer, nullable=False)
    duration = Column(Integer, nullable=False)  # seconds
    form_accuracy = Column(Float, nullable=False)  # 0.0 - 1.0
    form_corrections = Column(JSON, nullable=False, server_default='[]')
    calories_burned = Column(Float, nullable=False)
    order_index = Column(Integer, nullable=False)

    # Relationships
    workout_session = relationship("WorkoutSession", back_populates="exercises")

    def __repr__(self):
        return f"<ExercisePerformance(id={self.id}, type={self.exercise_type}, reps={self.reps})>"
