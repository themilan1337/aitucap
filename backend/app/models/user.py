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

    # Fitness data
    age = Column(Integer, nullable=True)
    weight = Column(Float, nullable=True)  # kg
    height = Column(Integer, nullable=True)  # cm
    fitness_goal = Column(String(50), nullable=True)  # 'lose_weight' | 'get_toned' | 'improve_shape'
    fitness_level = Column(String(50), nullable=True)  # 'beginner' | 'intermediate' | 'advanced'

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
