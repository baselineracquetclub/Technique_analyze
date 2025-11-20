import cv2
import mediapipe as mp
from typing import Optional, List

mp_pose = mp.solutions.pose


def detect_pose(image_path: str) -> Optional[List[mp_pose.PoseLandmark]]:
    """Run pose detection on a single frame.

    Returns a list of landmarks (or None if nothing detected).
    """
    img = cv2.imread(image_path)
    if img is None:
        return None

    img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

    with mp_pose.Pose(static_image_mode=True) as pose:
        res = pose.process(img_rgb)

    if not res.pose_landmarks:
        return None

    return res.pose_landmarks.landmark

