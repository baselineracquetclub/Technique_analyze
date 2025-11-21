from typing import List, Optional, Dict


# MediaPipe pose indices for reference:
# 11 = left_shoulder, 12 = right_shoulder
# 13 = left_elbow,   14 = right_elbow
# 15 = left_wrist,   16 = right_wrist
# 23 = left_hip,     24 = right_hip
# 25 = left_knee,    26 = right_knee
# 27 = left_ankle,   28 = right_ankle


def _shoulder_hip_rotation(pose) -> float:
    """
    Approximate shoulder vs hip rotation (in degrees of "twist").
    We measure how much the shoulder line is rotated relative to the hip line.
    """
    import numpy as np

    left_sh = pose[11]
    right_sh = pose[12]
    left_hip = pose[23]
    right_hip = pose[24]

    # Vectors: hips and shoulders
    hips = np.array([right_hip.x - left_hip.x, right_hip.y - left_hip.y])
    shoulders = np.array([right_sh.x - left_sh.x, right_sh.y - left_sh.y])

    # Angle between hips and shoulders
    denom = (np.linalg.norm(hips) * np.linalg.norm(shoulders)) or 1e-6
    cos_angle = float(hips @ shoulders / denom)
    cos_angle = max(-1.0, min(1.0, cos_angle))
    angle = float(np.degrees(np.arccos(cos_angle)))
    return angle


def _arm_extension(pose, right_handed: bool = True) -> float:
    """
    Distance from hitting shoulder to hitting wrist (2D).
    Larger distance ~ more extension (good proxy for contact frame).
    """
    import numpy as np

    if right_handed:
        shoulder = pose[12]
        wrist = pose[16]
    else:
        shoulder = pose[11]
        wrist = pose[15]

    return float(
        np.linalg.norm(
            [wrist.x - shoulder.x, wrist.y - shoulder.y]
        )
    )


def detect_forehand_phases(
    poses: List[Optional[list]],
    right_handed: bool = True,
) -> Dict[str, Optional[int]]:
    """
    Given a list of pose landmark lists (one per frame), pick indices for:
    - ready
    - unit_turn
    - contact
    - follow_through

    This is heuristic and assumes a simple, single-stroke clip.
    """
    valid_indices = [i for i, p in enumerate(poses) if p is not None]
    if len(valid_indices) < 2:
        # Not enough data
        return {
            "ready": valid_indices[0] if valid_indices else None,
            "unit_turn": None,
            "contact": None,
            "follow_through": None,
        }

    # 1) READY: earliest frame with some stance (just use first valid)
    ready_idx = valid_indices[0]

    # 2) UNIT TURN: frame (early in sequence) with strong shoulder/hip rotation
    shoulder_rotations = []
    for i in valid_indices:
        try:
            angle = _shoulder_hip_rotation(poses[i])
        except Exception:
            angle = 0.0
        shoulder_rotations.append((i, angle))

    # Sort by frame index (early first), then pick early frame with high rotation
    shoulder_rotations.sort(key=lambda x: x[0])
    if shoulder_rotations:
        # Take top rotation among the first half of frames
        half = max(1, len(shoulder_rotations) // 2)
        early_half = shoulder_rotations[:half]
        unit_turn_idx = max(early_half, key=lambda x: x[1])[0]
    else:
        unit_turn_idx = None

    # 3) CONTACT: frame with max arm extension (hitting arm)
    extensions = []
    for i in valid_indices:
        try:
            ext = _arm_extension(poses[i], right_handed=right_handed)
        except Exception:
            ext = 0.0
        extensions.append((i, ext))

    contact_idx = max(extensions, key=lambda x: x[1])[0] if extensions else None

    # 4) FOLLOW-THROUGH: later frame where arm is still fairly extended
    follow_through_idx = None
    if contact_idx is not None:
        later = [x for x in extensions if x[0] > contact_idx]
        if later:
            follow_through_idx = max(later, key=lambda x: x[1])[0]

    return {
        "ready": ready_idx,
        "unit_turn": unit_turn_idx,
        "contact": contact_idx,
        "follow_through": follow_through_idx,
    }
