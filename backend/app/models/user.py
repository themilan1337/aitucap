from sqlalchemy import Column, String, Integer, Float, Boolean, DateTime, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
import uuid

from app.database import Base


class User(Base):
    """User model for authentication"""

    __tablename__ = "users"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    email = Column(String(255), unique=True, nullable=False, index=True)
    full_name = Column(String(255), nullable=True)
    avatar_url = Column(String, nullable=True)

    # OAuth fields
    oauth_provider = Column(String(50), nullable=False)  # 'google'
    oauth_id = Column(String(255), unique=True, nullable=False, index=True)

    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    # Relationships
    profile = relationship("UserProfile", back_populates="user", uselist=False, cascade="all, delete-orphan")
    workout_plans = relationship("WorkoutPlan", back_populates="user", cascade="all, delete-orphan")
    workout_sessions = relationship("WorkoutSession", back_populates="user", cascade="all, delete-orphan")
    user_achievements = relationship("UserAchievement", back_populates="user", cascade="all, delete-orphan")

    def __repr__(self):
        return f"<User(id={self.id}, email={self.email}, provider={self.oauth_provider})>"


class UserProfile(Base):
    """User profile with fitness data"""

    __tablename__ = "user_profiles"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"), nullable=False, unique=True)

    # Basic data
    age = Column(Integer, nullable=True)
    weight = Column(Float, nullable=True)  # kg
    height = Column(Integer, nullable=True)  # cm
    gender = Column(String(20), nullable=True)  # 'male' | 'female' | 'other'

    # Body metrics (for more accurate plan generation)
    target_weight = Column(Float, nullable=True)  # kg - desired weight
    body_fat_percentage = Column(Float, nullable=True)  # % - optional

    # Fitness data
    fitness_goal = Column(String(50), nullable=True)  # 'lose_weight' | 'gain_muscle' | 'get_toned' | 'improve_endurance' | 'maintain'
    fitness_level = Column(String(50), nullable=True)  # 'beginner' | 'intermediate' | 'advanced'

    # Activity & Availability
    activity_level = Column(String(50), nullable=True)  # 'sedentary' | 'lightly_active' | 'moderately_active' | 'very_active'
    weekly_workout_days = Column(Integer, nullable=True)  # 3-7 days per week
    workout_duration_preference = Column(Integer, nullable=True)  # minutes per session (15, 30, 45, 60)

    # Health considerations
    has_injuries = Column(Boolean, default=False)
    injury_details = Column(String(500), nullable=True)  # Description of injuries or limitations
    medical_conditions = Column(String(500), nullable=True)  # Relevant medical conditions

    # Equipment availability
    has_equipment = Column(Boolean, default=False)
    available_equipment = Column(String(500), nullable=True)  # Comma-separated list

    # Preferences
    preferred_units = Column(String(10), default="metric")  # 'metric' | 'imperial'
    language = Column(String(10), default="ru")  # 'ru' | 'en'
    notifications_enabled = Column(Boolean, default=True)

    # Timestamps
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    # Relationships
    user = relationship("User", back_populates="profile")

    def __repr__(self):
        return f"<UserProfile(user_id={self.user_id}, goal={self.fitness_goal}, level={self.fitness_level})>"
