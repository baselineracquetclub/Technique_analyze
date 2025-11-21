from typing import List, Optional, Dict


def _shoulder_hip_rotation(pose) -> float:
    """Approximate shoulder vs hip rotation (degrees)."""
    import numpy as np

    left_sh = pose[11]
    right_sh = pose[12]
    left_hip = pose[23]
    right_hip = pose[24]

    hips = np.array([right_hip.x - left_hip.x, right_hip.y - left_hip.y])
    shoulders = np.array([right_sh.x - left_sh.x, right_sh.y - left_sh.y])

    denom = (np.linalg.norm(hips) * np.linalg.norm(shoulders)) or 1e-6
    cos_angle = float(hips @ shoulders / denom)
    cos_angle = max(-1.0, min(1.0, cos_angle))
    angle = float(np.degrees(np.arccos(cos_angle)))
    return angle


def _arm_extension(pose, right_handed: bool = True) -> float:
    """Distance between hitting shoulder and hitting wrist (2D)."""
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
    """Pick indices for ready, unit_turn, contact, follow_through.

    Heuristic: we assume a short clip with a single forehand from a side-ish view.
    """
    valid_indices = [i for i, p in enumerate(poses) if p is not None]
    if len(valid_indices) < 2:
        return {
            "ready": valid_indices[0] if valid_indices else None,
            "unit_turn": None,
            "contact": None,
            "follow_through": None,
        }

    # 1) READY = first valid frame
    ready_idx = valid_indices[0]

    # 2) UNIT TURN: early frame with strong shoulder/hip rotation
    shoulder_rotations = []
    for i in valid_indices:
        try:
            angle = _shoulder_hip_rotation(poses[i])
        except Exception:
            angle = 0.0
        shoulder_rotations.append((i, angle))

    shoulder_rotations.sort(key=lambda x: x[0])
    half = max(1, len(shoulder_rotations) // 2)
    early_half = shoulder_rotations[:half]
    unit_turn_idx = max(early_half, key=lambda x: x[1])[0]

    # 3) CONTACT: frame with max arm extension
    extensions = []
    for i in valid_indices:
        try:
            ext = _arm_extension(poses[i], right_handed=right_handed)
        except Exception:
            ext = 0.0
        extensions.append((i, ext))

    contact_idx = max(extensions, key=lambda x: x[1])[0]

    # 4) FOLLOW THROUGH: later frame with still-large extension
    later = [x for x in extensions if x[0] > contact_idx]
    follow_through_idx = max(later, key=lambda x: x[1])[0] if later else None

    return {
        "ready": ready_idx,
        "unit_turn": unit_turn_idx,
        "contact": contact_idx,
        "follow_through": follow_through_idx,
    }

