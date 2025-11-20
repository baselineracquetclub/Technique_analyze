from fastapi import FastAPI, UploadFile, File, Form
from fastapi.middleware.cors import CORSMiddleware
from typing import Dict
import tempfile
import os

from analysis.frame_extractor import extract_key_frames
from analysis.pose_detector import detect_pose
from analysis.metrics import compute_metrics
from rules.coaching_rules import generate_suggestions

app = FastAPI(title="Tennis Technique Analyzer")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def root():
    return {"status": "ok", "message": "Tennis Technique Analyzer backend running"}


@app.post("/analyze")
async def analyze_video(
    file: UploadFile = File(...),
    student_name: str = Form(...),
    stroke_type: str = Form(...)
) -> Dict:
    """Accept a video, extract frames, run pose + metrics, return suggestions."""
    # 1. Save uploaded video to a temp file
    with tempfile.NamedTemporaryFile(delete=False, suffix=".mp4") as tmp:
        contents = await file.read()
        tmp.write(contents)
        video_path = tmp.name

    # 2. Extract a small set of key frames (very simple sampling for now)
    frames = extract_key_frames(video_path)

    # 3. Run pose detection on each frame
    poses = [detect_pose(f) for f in frames]

    # 4. Compute simple metrics from poses
    metrics = compute_metrics(poses)

    # 5. Generate coaching suggestions based on metrics
    suggestions = generate_suggestions(metrics, stroke_type)

    # 6. Clean up video file (frames are still on disk)
    try:
        os.remove(video_path)
    except OSError:
        pass

    return {
        "student": student_name,
        "stroke": stroke_type,
        "frames": frames,
        "metrics": metrics,
        "suggestions": suggestions,
    }

