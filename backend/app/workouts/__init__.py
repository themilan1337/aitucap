"""
Workout services for pose detection and exercise counting.
"""
from .exercise_counter import ExerciseCounter
from .rtmpose_processor import RTMPoseProcessor, get_rtmpose_processor

__all__ = ['ExerciseCounter', 'RTMPoseProcessor', 'get_rtmpose_processor']
