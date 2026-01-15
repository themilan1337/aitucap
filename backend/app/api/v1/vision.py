"""
Vision API for real-time pose detection and exercise tracking.
Uses WebSocket for low-latency video frame processing.
"""
import os
import base64
import json
import logging
import numpy as np
import cv2
from fastapi import APIRouter, WebSocket, WebSocketDisconnect, HTTPException
from fastapi.responses import JSONResponse
from typing import Dict, Any
from app.workouts import get_rtmpose_processor

logger = logging.getLogger(__name__)

router = APIRouter()

# Get paths
BACKEND_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))
MODELS_DIR = os.path.join(BACKEND_DIR, 'models')
EXERCISES_CONFIG = os.path.join(BACKEND_DIR, 'data', 'exercises.json')

# Initialize processor (singleton pattern)
processor = None


def get_processor():
    """Get or initialize RTMPose processor"""
    global processor
    if processor is None:
        try:
            processor = get_rtmpose_processor(
                models_dir=MODELS_DIR,
                exercises_config_path=EXERCISES_CONFIG,
                mode='balanced'  # Can be: 'lightweight', 'balanced', 'performance'
            )
            logger.info("✓ RTMPose processor initialized successfully")
        except Exception as e:
            logger.error(f"✗ Failed to initialize RTMPose processor: {e}")
            raise
    return processor


@router.get("/health")
async def health_check():
    """Check if vision API is ready"""
    try:
        proc = get_processor()
        return {
            "status": "healthy",
            "pose_detection": "ready",
            "models_dir": MODELS_DIR,
            "exercises_config": EXERCISES_CONFIG
        }
    except Exception as e:
        logger.error(f"Health check failed: {e}")
        raise HTTPException(status_code=503, detail=f"Vision API not ready: {str(e)}")


@router.get("/exercises")
async def list_exercises():
    """Get list of supported exercises"""
    try:
        with open(EXERCISES_CONFIG, 'r', encoding='utf-8') as f:
            data = json.load(f)
            exercises = []
            for ex_id, ex_data in data.get('exercises', {}).items():
                exercises.append({
                    "id": ex_id,
                    "name_ru": ex_data.get("name_ru"),
                    "name_en": ex_data.get("name_en"),
                    "is_leg_exercise": ex_data.get("is_leg_exercise", False)
                })
            return {"exercises": exercises}
    except Exception as e:
        logger.error(f"Failed to load exercises: {e}")
        raise HTTPException(status_code=500, detail="Failed to load exercises")


@router.websocket("/ws/pose")
async def websocket_pose_detection(websocket: WebSocket):
    """
    WebSocket endpoint for real-time pose detection.

    Client sends: JSON with { "frame": "base64_image", "exercise": "squat" }
    Server responds: JSON with { "keypoints": [[x,y], ...], "reps": 10, "angle": 145.2, "angle_point": [[x1,y1], [x2,y2], [x3,y3]] }
    """
    await websocket.accept()
    logger.info("✓ WebSocket connection established")

    try:
        proc = get_processor()
        session_id = id(websocket)
        logger.info(f"Session {session_id}: Started")

        while True:
            try:
                # Receive message from client
                data = await websocket.receive_text()
                message = json.loads(data)

                # Extract frame and exercise type
                frame_b64 = message.get("frame")
                exercise_type = message.get("exercise", "squat")

                if not frame_b64:
                    await websocket.send_json({
                        "error": "Missing 'frame' in message"
                    })
                    continue

                # Decode base64 image
                try:
                    # Remove data URL prefix if present
                    if ',' in frame_b64:
                        frame_b64 = frame_b64.split(',')[1]

                    img_data = base64.b64decode(frame_b64)
                    nparr = np.frombuffer(img_data, np.uint8)
                    frame = cv2.imdecode(nparr, cv2.IMREAD_COLOR)

                    if frame is None:
                        await websocket.send_json({
                            "error": "Failed to decode image"
                        })
                        continue

                except Exception as e:
                    logger.error(f"Image decode error: {e}")
                    await websocket.send_json({
                        "error": f"Image decode error: {str(e)}"
                    })
                    continue

                # Process frame with RTMPose
                try:
                    current_angle, angle_point, keypoints = proc.process_frame(
                        frame,
                        exercise_type
                    )

                    # Prepare response
                    response: Dict[str, Any] = {
                        "success": True,
                        "exercise": exercise_type,
                        "reps": proc.exercise_counter.get_counter(),
                        "stage": proc.exercise_counter.get_stage(),
                        "form_corrections": proc.exercise_counter.get_form_corrections()
                    }

                    # Add keypoints if detected
                    if keypoints is not None:
                        # Convert numpy arrays to lists for JSON serialization
                        keypoints_list = keypoints.tolist()
                        response["keypoints"] = keypoints_list
                        response["detected"] = True
                    else:
                        response["detected"] = False

                    # Add angle info if available
                    if current_angle is not None:
                        response["angle"] = round(float(current_angle), 1)

                    if angle_point is not None:
                        response["angle_point"] = angle_point

                    # Send response
                    await websocket.send_json(response)

                except Exception as e:
                    logger.error(f"Frame processing error: {e}")
                    await websocket.send_json({
                        "error": f"Processing error: {str(e)}",
                        "success": False
                    })

            except json.JSONDecodeError as e:
                logger.error(f"JSON decode error: {e}")
                await websocket.send_json({
                    "error": "Invalid JSON format"
                })

    except WebSocketDisconnect:
        logger.info(f"Session {session_id}: WebSocket disconnected")
    except Exception as e:
        logger.error(f"Session {session_id}: Unexpected error: {e}")
    finally:
        # Reset counter when session ends
        if proc:
            proc.exercise_counter.reset_counter()
        logger.info(f"Session {session_id}: Ended")


@router.post("/reset-counter")
async def reset_counter():
    """Reset the exercise counter"""
    try:
        proc = get_processor()
        proc.exercise_counter.reset_counter()
        return {"success": True, "message": "Counter reset"}
    except Exception as e:
        logger.error(f"Failed to reset counter: {e}")
        raise HTTPException(status_code=500, detail="Failed to reset counter")
