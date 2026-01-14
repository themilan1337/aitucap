"""
RTMPose pose detection processor for workout tracking.
Adapted from Good-GYM-master for FastAPI backend.
"""
import os
import cv2
import numpy as np
import json
from rtmlib import Wholebody
from typing import Optional, Tuple, List, Dict, Any
from .exercise_counter import ExerciseCounter


class RTMPoseProcessor:
    """RTMPose pose detection processor"""

    def __init__(
        self,
        exercise_counter: ExerciseCounter,
        models_dir: str,
        mode: str = 'balanced',
        backend: str = 'onnxruntime',
        device: str = 'cpu'
    ):
        self.exercise_counter = exercise_counter
        self.show_skeleton = True
        self.conf_threshold = 0.5
        self.device = device
        self.backend = backend
        self.models_dir = models_dir

        # Initialize RTMPose model
        self.wholebody = None
        self.init_rtmpose(mode)

        self.keypoint_mapping = self.get_keypoint_mapping()

        # Load exercise configurations for angle points
        self.exercise_configs = self.load_exercise_configs()

    def init_rtmpose(self, mode: str = 'balanced'):
        """Initialize RTMPose model"""
        try:
            print(f"Initializing RTMPose model (mode: {mode}, backend: {self.backend}, device: {self.device})")

            # Check if local model files exist
            if os.path.exists(self.models_dir):
                # Try to use local models
                det_model = os.path.join(self.models_dir, 'yolox_nano_8xb8-300e_humanart-40f6f0d0.onnx')

                # Select different pose detection models based on mode
                if mode == 'lightweight':
                    pose_model = os.path.join(self.models_dir,
                                              'rtmpose-t_simcc-body7_pt-body7_420e-256x192-026a1439_20230504.onnx')
                    pose_input_size = (192, 256)
                elif mode == 'performance':
                    pose_model = os.path.join(self.models_dir,
                                              'rtmpose-m_simcc-body7_pt-body7_420e-256x192-e48f03d0_20230504.onnx')
                    pose_input_size = (192, 256)
                else:  # balanced
                    pose_model = os.path.join(self.models_dir,
                                              'rtmpose-s_simcc-body7_pt-body7_420e-256x192-acd4a1ef_20230504.onnx')
                    pose_input_size = (192, 256)

                if os.path.exists(det_model) and os.path.exists(pose_model):
                    print(f"✓ Using local model files ({mode} mode)")
                    self.wholebody = Wholebody(
                        det=det_model,
                        det_input_size=(416, 416),
                        pose=pose_model,
                        pose_input_size=pose_input_size,
                        backend=self.backend,
                        device=self.device
                    )
                    print("✓ RTMPose local model initialization successful")
                    return
                else:
                    print("⚠ Local model files incomplete, using online download")
            else:
                print(f"⚠ models directory doesn't exist at {self.models_dir}, using online download")

            # Fallback to online download
            self.wholebody = Wholebody(
                mode=mode,
                backend=self.backend,
                device=self.device
            )
            print("✓ RTMPose online model initialization successful")

        except Exception as e:
            print(f"✗ RTMPose initialization failed: {e}")
            raise

    def get_keypoint_mapping(self) -> List[int]:
        """Get keypoint mapping (COCO 17 keypoint format)"""
        # RTMPose uses COCO 17 keypoint format:
        # 0: nose, 1: left_eye, 2: right_eye, 3: left_ear, 4: right_ear
        # 5: left_shoulder, 6: right_shoulder, 7: left_elbow, 8: right_elbow
        # 9: left_wrist, 10: right_wrist, 11: left_hip, 12: right_hip
        # 13: left_knee, 14: right_knee, 15: left_ankle, 16: right_ankle
        return list(range(17))  # 1:1 mapping

    def load_exercise_configs(self) -> Dict[str, Any]:
        """Load exercise configurations from JSON file"""
        exercises_file = os.path.join(os.path.dirname(self.models_dir), 'data', 'exercises.json')

        try:
            if os.path.exists(exercises_file):
                with open(exercises_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    exercises = data.get('exercises', {})

                    # Extract angle_point for each exercise
                    configs = {}
                    for exercise_type, config in exercises.items():
                        configs[exercise_type] = {
                            'angle_point': config.get('angle_point', [])
                        }

                    return configs
            else:
                print(f"⚠ Exercises file not found at {exercises_file}")
                return {}
        except Exception as e:
            print(f"✗ ERROR loading exercises from JSON: {e}")
            return {}

    def update_model(self, mode: str = 'balanced'):
        """Update model"""
        print(f"Updating RTMPose model to mode: {mode}")
        self.init_rtmpose(mode)
        print(f"✓ RTMPose processor updated to mode: {mode}")

    def process_frame(
        self,
        frame: np.ndarray,
        exercise_type: str
    ) -> Tuple[Optional[float], Optional[List], Optional[np.ndarray]]:
        """
        Process single frame for pose detection and exercise counting.

        Returns:
            Tuple of (current_angle, angle_point, keypoints)
        """
        # Size check, resize if frame is too large
        h, w = frame.shape[:2]
        original_size = (w, h)

        # RTMPose is suitable for higher resolution, but limit for performance
        if w > 640 or h > 640:
            scale = min(640 / w, 640 / h)
            frame = cv2.resize(frame, (int(w * scale), int(h * scale)))
            scale_factor = scale
        else:
            scale_factor = 1.0

        # Initialize results
        current_angle = None
        angle_point = None
        keypoints = None

        try:
            # Use RTMPose for pose detection
            detected_keypoints, scores = self.wholebody(frame)

            # Process results
            if detected_keypoints is not None and len(detected_keypoints) > 0:
                # Get first person's keypoints (highest confidence)
                keypoints = detected_keypoints[0]  # shape: (17, 2)
                confidence_scores = scores[0] if scores is not None else None

                # Filter low confidence keypoints
                if confidence_scores is not None:
                    valid_mask = confidence_scores > self.conf_threshold
                    keypoints[~valid_mask] = [0, 0]  # Set low confidence points to (0,0)

                # If need to scale back to original size
                if scale_factor != 1.0:
                    keypoints = keypoints / scale_factor

                # Get corresponding angle and joint points based on exercise type
                current_angle, angle_point = self.get_exercise_angle(keypoints, exercise_type)

        except Exception as e:
            print(f"✗ RTMPose processing failed: {e}")

        # Return current_angle, angle_point, and keypoints
        return current_angle, angle_point, keypoints

    def get_exercise_angle(
        self,
        keypoints: np.ndarray,
        exercise_type: str
    ) -> Tuple[Optional[float], Optional[List]]:
        """Get angle based on exercise type"""
        current_angle = None
        angle_point = None

        try:
            # Get the counting method based on exercise type
            count_method_map = {
                "squat": self.exercise_counter.count_squat,
                "pushup": self.exercise_counter.count_pushup,
                "situp": self.exercise_counter.count_situp,
                "bicep_curl": self.exercise_counter.count_bicep_curl,
                "lateral_raise": self.exercise_counter.count_lateral_raise,
                "overhead_press": self.exercise_counter.count_overhead_press,
                "leg_raise": self.exercise_counter.count_leg_raise,
                "knee_raise": self.exercise_counter.count_knee_raise,
                "knee_press": self.exercise_counter.count_knee_press,
                "crunch": self.exercise_counter.count_crunch
            }

            # Get counting method
            count_method = count_method_map.get(exercise_type)
            if count_method:
                current_angle = count_method(keypoints)

                # Get angle_point from config
                if current_angle is not None and exercise_type in self.exercise_configs:
                    angle_point_indices = self.exercise_configs[exercise_type].get('angle_point', [])
                    if len(angle_point_indices) == 3:
                        angle_point = [
                            keypoints[angle_point_indices[0]].tolist(),
                            keypoints[angle_point_indices[1]].tolist(),
                            keypoints[angle_point_indices[2]].tolist()
                        ]
        except Exception as e:
            print(f"✗ Error calculating exercise angle: {e}")

        return current_angle, angle_point

    def set_skeleton_visibility(self, show: bool):
        """Set skeleton display state"""
        self.show_skeleton = show
        print(f"RTMPose skeleton display: {'On' if show else 'Off'}")


# Singleton instance holder
_rtmpose_processor_instance: Optional[RTMPoseProcessor] = None


def get_rtmpose_processor(
    models_dir: str,
    exercises_config_path: str,
    mode: str = 'balanced'
) -> RTMPoseProcessor:
    """Get or create RTMPose processor singleton"""
    global _rtmpose_processor_instance

    if _rtmpose_processor_instance is None:
        # Create exercise counter first
        exercise_counter = ExerciseCounter(exercises_config_path)

        # Create RTMPose processor
        _rtmpose_processor_instance = RTMPoseProcessor(
            exercise_counter=exercise_counter,
            models_dir=models_dir,
            mode=mode
        )

    return _rtmpose_processor_instance
