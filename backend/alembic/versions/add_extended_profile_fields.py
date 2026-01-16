"""add extended user profile fields

Revision ID: add_extended_profile_fields
Revises: ebae4cabb574
Create Date: 2026-01-16 21:00:00.000000

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'add_extended_profile_fields'
down_revision = 'ebae4cabb574'
branch_labels = None
depends_on = None


def upgrade():
    # Add new columns to user_profiles table
    op.add_column('user_profiles', sa.Column('gender', sa.String(length=20), nullable=True))
    op.add_column('user_profiles', sa.Column('target_weight', sa.Float(), nullable=True))
    op.add_column('user_profiles', sa.Column('body_fat_percentage', sa.Float(), nullable=True))
    op.add_column('user_profiles', sa.Column('activity_level', sa.String(length=50), nullable=True))
    op.add_column('user_profiles', sa.Column('weekly_workout_days', sa.Integer(), nullable=True))
    op.add_column('user_profiles', sa.Column('workout_duration_preference', sa.Integer(), nullable=True))
    op.add_column('user_profiles', sa.Column('has_injuries', sa.Boolean(), server_default='false'))
    op.add_column('user_profiles', sa.Column('injury_details', sa.String(length=500), nullable=True))
    op.add_column('user_profiles', sa.Column('medical_conditions', sa.String(length=500), nullable=True))
    op.add_column('user_profiles', sa.Column('has_equipment', sa.Boolean(), server_default='false'))
    op.add_column('user_profiles', sa.Column('available_equipment', sa.String(length=500), nullable=True))


def downgrade():
    # Remove added columns
    op.drop_column('user_profiles', 'available_equipment')
    op.drop_column('user_profiles', 'has_equipment')
    op.drop_column('user_profiles', 'medical_conditions')
    op.drop_column('user_profiles', 'injury_details')
    op.drop_column('user_profiles', 'has_injuries')
    op.drop_column('user_profiles', 'workout_duration_preference')
    op.drop_column('user_profiles', 'weekly_workout_days')
    op.drop_column('user_profiles', 'activity_level')
    op.drop_column('user_profiles', 'body_fat_percentage')
    op.drop_column('user_profiles', 'target_weight')
    op.drop_column('user_profiles', 'gender')
