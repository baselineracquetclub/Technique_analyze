import cv2
import tempfile
from typing import List


def extract_key_frames(video_path: str, num_frames: int = 6) -> List[str]:
    """Very simple frame sampler: grab `num_frames` evenly spaced frames.

    Returns a list of temporary image file paths.
    """
    cap = cv2.VideoCapture(video_path)
    total = int(cap.get(cv2.CAP_PROP_FRAME_COUNT)) or 1

    sample_indices = [int(total * i / num_frames) for i in range(num_frames)]
    saved_paths = []

    for idx, frame_idx in enumerate(sample_indices):
        cap.set(cv2.CAP_PROP_POS_FRAMES, frame_idx)
        ret, frame = cap.read()
        if not ret:
            continue
        tmp = tempfile.NamedTemporaryFile(delete=False, suffix=f"_frame_{idx}.jpg")
        cv2.imwrite(tmp.name, frame)
        saved_paths.append(tmp.name)

    cap.release()
    return saved_paths

