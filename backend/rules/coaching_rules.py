from typing import Dict, Any


def _add(msgs: list, text: str):
    if text not in msgs:
        msgs.append(text)


def generate_suggestions(metrics: Dict[str, Any], stroke: str) -> Dict[str, list]:
    """
    Turn numeric metrics into coach-style feedback.

    Currently tuned for FOREHAND.
    """
    doing_well: list = []
    work_on: list = []

    stroke = (stroke or "").lower()

    phases = metrics.get("phases", {})
    ready = metrics.get("ready", {})
    unit_turn = metrics.get("unit_turn", {})
    contact = metrics.get("contact", {})
    follow = metrics.get("follow_through", {})

    # ---- READY POSITION ----
    stance = ready.get("stance_width")
    if stance is not None:
        # these thresholds will depend on camera distance; tweak as you test
        if stance < 0.07:
            _add(work_on, "Widen your stance in your ready position for more stability and quicker movement.")
        elif 0.07 <= stance <= 0.16:
            _add(doing_well, "Nice, athletic stance width in your ready position.")
        else:
            _add(work_on, "Your stance is quite wide; make sure it still feels comfortable and lets you move explosively.")

    ready_knee = ready.get("front_knee_angle_deg")
    if ready_knee is not None:
        if ready_knee > 165:
            _add(work_on, "Bend your knees a bit more in your ready position so you stay lower and more explosive.")
        elif 135 <= ready_knee <= 160:
            _add(doing_well, "Good knee bend in your ready position, helping balance and quick reactions.")
        elif ready_knee < 120:
            _add(work_on, "You are bending very low in your ready stance; make sure that depth still feels efficient and not tiring.")

    # ---- UNIT TURN / PREPARATION ----
    shoulder_turn = unit_turn.get("shoulder_turn_deg")
    if shoulder_turn is not None:
        if shoulder_turn < 20:
            _add(work_on, "Turn your shoulders earlier on the forehand so your body, not just your arm, powers the stroke.")
        elif 20 <= shoulder_turn <= 45:
            _add(doing_well, "Solid shoulder turn on your forehand preparation.")
        else:
            _add(doing_well, "Great upper body coil on the forehand—lots of stored power.")

    # ---- CONTACT ----
    contact_knee = contact.get("front_knee_angle_deg")
    if contact_knee is not None:
        if contact_knee > 165:
            _add(work_on, "Bend your front knee more as you move into contact to use your legs for power and stability.")
        elif 135 <= contact_knee <= 160:
            _add(doing_well, "Good use of your legs into the ball at contact.")
        elif contact_knee < 120:
            _add(work_on, "You are very low at contact; make sure the extra bend is helping, not slowing, your recovery.")

    height = contact.get("contact_height_rel")
    if height is not None:
        if height < 0.3:
            _add(work_on, "You're making contact very low; try to take the ball a bit earlier or higher when possible.")
        elif 0.3 <= height <= 0.7:
            _add(doing_well, "Nice comfortable contact height on your forehand.")
        else:
            _add(work_on, "You're contacting the ball quite high; make sure you are still able to swing up and through comfortably.")

    lateness = contact.get("contact_lateness")
    if lateness is not None:
        # Positive = more in front (for typical right-handed camera view)
        if lateness < -0.02:
            _add(work_on, "The ball is getting a bit too far back on your forehand; aim to meet it more out in front of your body.")
        elif -0.02 <= lateness <= 0.04:
            _add(doing_well, "Good contact point relative to your body—nicely in front.")
        else:
            _add(work_on, "You're contacting the ball very far in front; make sure you're not overreaching and losing balance.")

    # ---- FOLLOW THROUGH ----
    follow_turn = follow.get("shoulder_turn_deg")
    if follow_turn is not None:
        if follow_turn < 20:
            _add(work_on, "Let your torso rotate more through the ball on the follow-through so the swing finishes freely.")
        elif 20 <= follow_turn <= 50:
            _add(doing_well, "Nice, relaxed body rotation through your forehand follow-through.")
        else:
            _add(doing_well, "Big rotation through the shot—great for power, as long as you stay balanced.")

    # If stroke is not a forehand, keep feedback generic for now
    if "forehand" not in stroke and not doing_well and not work_on:
        _add(work_on, "This version of the analyzer is currently tuned for forehands. Try selecting 'forehand' for more specific feedback.")

    if not doing_well and not work_on:
        _add(work_on, "Upload a clear, single-stroke forehand clip from the side for more precise feedback.")

    return {
        "doing_well": doing_well,
        "work_on": work_on,
    }
