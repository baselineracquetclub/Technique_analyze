from typing import Dict, Any


def generate_suggestions(metrics: Dict[str, Any], stroke: str) -> Dict[str, list]:
    """Turn simple numeric metrics into coach-style feedback."""
    good = []
    work_on = []

    ready = metrics.get("ready", {})

    # Stance width heuristic
    stance = ready.get("stance_width_ratio")
    if stance is not None:
        if stance < 0.08:
            work_on.append(
                "Widen your stance in your ready position for better balance and quicker movement."
            )
        elif stance > 0.18:
            good.append("Nice wide, athletic stance in your ready position.")
        else:
            good.append("Your stance width is in a solid, playable range.")

    # Knee angle heuristic
    knee_angle = ready.get("knee_angle_deg")
    if knee_angle is not None:
        if knee_angle > 160:
            work_on.append(
                "Bend your knees a bit more to stay lower and use your legs for power."
            )
        elif 130 <= knee_angle <= 155:
            good.append("Good knee bend helping your stability and explosiveness.")
        elif knee_angle < 120:
            work_on.append(
                "You're bending very deep—make sure it still feels comfortable and efficient."
            )

    if not good and not work_on:
        work_on.append(
            "Upload a clearer video with a single stroke for more precise feedback."
        )

    return {
        "doing_well": good,
        "work_on": work_on,
    }

