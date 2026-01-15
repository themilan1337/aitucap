from sqlalchemy import Column, String, Integer, Boolean, DateTime, Date, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
import uuid

from app.database import Base


class WorkoutPlan(Base):
    """Workout plan (supports any duration: 7, 30, or custom days)"""

    __tablename__ = "weekly_plans"  # Keep table name for backward compatibility

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    week_start_date = Column(Date, nullable=False)  # Actually plan_start_date now
    is_active = Column(Boolean, default=True, index=True)
    generated_by_ai = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    # Relationships
    user = relationship("User", back_populates="workout_plans")
    days = relationship("PlanDay", back_populates="plan", cascade="all, delete-orphan", order_by="PlanDay.day_number")

    def __repr__(self):
        return f"<WorkoutPlan(id={self.id}, user_id={self.user_id}, start={self.week_start_date})>"


class PlanDay(Base):
    """Individual day in a workout plan"""

    __tablename__ = "plan_days"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    plan_id = Column(UUID(as_uuid=True), ForeignKey("weekly_plans.id", ondelete="CASCADE"), nullable=False, index=True)
    day_number = Column(Integer, nullable=False)  # 0-29 for 30-day plans (or 0-6 for legacy 7-day)
    date = Column(Date, nullable=False, index=True)
    is_rest_day = Column(Boolean, default=False)
    is_completed = Column(Boolean, default=False)
    completed_at = Column(DateTime(timezone=True), nullable=True)

    # Relationships
    plan = relationship("WorkoutPlan", back_populates="days")
    exercises = relationship("PlannedExercise", back_populates="plan_day", cascade="all, delete-orphan", order_by="PlannedExercise.order_index")
    workout_sessions = relationship("WorkoutSession", back_populates="plan_day")

    def __repr__(self):
        return f"<PlanDay(id={self.id}, date={self.date}, is_rest={self.is_rest_day})>"


class PlannedExercise(Base):
    """Exercise planned for a specific day"""

    __tablename__ = "planned_exercises"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    plan_day_id = Column(UUID(as_uuid=True), ForeignKey("plan_days.id", ondelete="CASCADE"), nullable=False, index=True)
    exercise_type = Column(String(50), nullable=False)  # 'squat' | 'lunge' | 'pushup' | 'plank'
    target_sets = Column(Integer, nullable=False)
    target_reps = Column(Integer, nullable=False)
    estimated_minutes = Column(Integer, nullable=False)
    order_index = Column(Integer, nullable=False)

    # Relationships
    plan_day = relationship("PlanDay", back_populates="exercises")

    def __repr__(self):
        return f"<PlannedExercise(id={self.id}, type={self.exercise_type}, sets={self.target_sets}x{self.target_reps})>"


# Backward compatibility alias
WeeklyPlan = WorkoutPlan
