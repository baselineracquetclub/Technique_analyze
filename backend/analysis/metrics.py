from typing import List, Dict, Any, Optional
import numpy as np

from .keyframes import detect_forehand_phases


def _angle(a, b, c) -> float:
    """Compute the angle ABC (in degrees) given three landmarks."""
    a = np.array([a.x, a.y])
    b = np.array([b.x, b.y])
    c = np.array([c.x, c.y])
    ba = a - b
    bc = c - b
    denom = (np.linalg.norm(ba) * np.linalg.norm(bc)) or 1e-6
    cos_angle = float(ba @ bc / denom)
    cos_angle = max(-1.0, min(1.0, cos_angle))
    return float(np.degrees(np.arccos(cos_angle)))


def _stance_width(pose) -> float:
    """Approximate stance width using hip x-distance (normalized units)."""
    left_hip = pose[23]
    right_hip = pose[24]
    return float(abs(left_hip.x - right_hip.x))


def _knee_bend(pose, right_leg: bool = True) -> float:
    """Knee angle of the front leg (bigger angle = straighter)."""
    # For a right-handed forehand with neutral stance, right leg is often back,
    # but we don't know camera view, so we just measure one side consistently.
    if right_leg:
        hip = pose[24]
        knee = pose[26]
        ankle = pose[28]
    else:
        hip = pose[23]
        knee = pose[25]
        ankle = pose[27]

    return _angle(hip, knee, ankle)


def _shoulder_turn(pose) -> float:
    """How much shoulders are rotated vs hips (proxy for unit turn power)."""
    left_sh = pose[11]
    right_sh = pose[12]
    left_hip = pose[23]
    right_hip = pose[24]

    shoulders = np.array([right_sh.x - left_sh.x, right_sh.y - left_sh.y])
    hips = np.array([right_hip.x - left_hip.x, right_hip.y - left_hip.y])

    denom = (np.linalg.norm(shoulders) * np.linalg.norm(hips)) or 1e-6
    cos_angle = float(shoulders @ hips / denom)
    cos_angle = max(-1.0, min(1.0, cos_angle))
    return float(np.degrees(np.arccos(cos_angle)))


def _contact_height(pose, right_handed: bool = True) -> float:
    """
    Height of hitting hand relative to body height (0 = feet, 1 = head-ish).
    """
    if right_handed:
        wrist = pose[16]
    else:
        wrist = pose[15]

    # Use ankle and head-ish (nose) to approximate vertical body span
    ankle = pose[27]  # left_ankle
    head = pose[0]    # nose

    body_height = abs(head.y - ankle.y) or 1e-6
    # y increases downward, so invert
    rel = (ankle.y - wrist.y) / body_height
    return float(rel)


def _contact_lateness(pose, right_handed: bool = True) -> float:
    """
    Very rough measure: how far in front of the hips the hitting wrist is.
    > 0 = in front, < 0 = jammed behind.
    """
    if right_handed:
        wrist = pose[16]
    else:
        wrist = pose[15]

    left_hip = pose[23]
    right_hip = pose[24]
    hip_center_x = (left_hip.x + right_hip.x) / 2.0

    return float(wrist.x - hip_center_x)


def compute_metrics(poses: List[Optional[list]]) -> Dict[str, Any]:
    """
    Compute metrics across multiple frames for a forehand.

    We:
    - detect phases (ready, unit_turn, contact, follow_through)
    - compute stance width, knee bend, shoulder turn, contact height, etc.
    """
    if not poses:
        return {}

    # Filter out completely missing
    valid = [p for p in poses if p is not None]
    if not valid:
        return {}

    # Assume right-handed for now
    right_handed = True

    phases = detect_forehand_phases(poses, right_handed=right_handed)

    def get_pose(idx: Optional[int]):
        if idx is None:
            return None
        if idx < 0 or idx >= len(poses):
            return None
        return poses[idx]

    ready_pose = get_pose(phases["ready"])
    unit_pose = get_pose(phases["unit_turn"])
    contact_pose = get_pose(phases["contact"])
    follow_pose = get_pose(phases["follow_through"])

    metrics: Dict[str, Any] = {
        "phases": phases,
        "ready": {},
        "unit_turn": {},
        "contact": {},
        "follow_through": {},
    }

    # READY PHASE METRICS
    if ready_pose is not None:
        metrics["ready"]["stance_width"] = _stance_width(ready_pose)
        metrics["ready"]["front_knee_angle_deg"] = _knee_bend(ready_pose, right_leg=True)

    # UNIT TURN METRICS
    if unit_pose is not None:
        metrics["unit_turn"]["shoulder_turn_deg"] = _shoulder_turn(unit_pose)

    # CONTACT METRICS
    if contact_pose is not None:
        metrics["contact"]["front_knee_angle_deg"] = _knee_bend(contact_pose, right_leg=True)
        metrics["contact"]["contact_height_rel"] = _contact_height(
            contact_pose, right_handed=right_handed
        )
        metrics["contact"]["contact_lateness"] = _contact_lateness(
            contact_pose, right_handed=right_handed
        )

    # FOLLOW-THROUGH METRICS (could expand later)
    if follow_pose is not None:
        metrics["follow_through"]["shoulder_turn_deg"] = _shoulder_turn(follow_pose)

    return metrics
