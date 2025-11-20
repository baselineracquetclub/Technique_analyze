from typing import List, Dict, Any, Optional
import numpy as np


def _angle(a, b, c) -> float:
    """Compute the angle ABC (in degrees) given three landmarks."""
    a = np.array([a.x, a.y])
    b = np.array([b.x, b.y])
    c = np.array([c.x, c.y])
    ba = a - b
    bc = c - b
    denom = (np.linalg.norm(ba) * np.linalg.norm(bc)) or 1e-6
    cos_angle = np.dot(ba, bc) / denom
    cos_angle = np.clip(cos_angle, -1.0, 1.0)
    return float(np.degrees(np.arccos(cos_angle)))


def compute_metrics(poses: List[Optional[list]]) -> Dict[str, Any]:
    """Compute simple metrics from a list of pose landmark lists.

    For now we just use the first pose as an approximation of 'ready'.
    Later you can extend this to detect real key phases.
    """
    if not poses:
        return {}

    pose = poses[0]
    if pose is None:
        return {}

    # MediaPipe pose indices:
    # 23 = left_hip, 24 = right_hip, 25 = left_knee, 27 = left_ankle
    left_hip = pose[23]
    right_hip = pose[24]
    left_knee = pose[25]
    left_ankle = pose[27]

    knee_angle = _angle(left_hip, left_knee, left_ankle)

    # Use hip x-distance as a proxy for stance width (normalized)
    stance_width = abs(left_hip.x - right_hip.x)

    return {
        "ready": {
            "knee_angle_deg": knee_angle,
            "stance_width_ratio": stance_width,
        }
    }

