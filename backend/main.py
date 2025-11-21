from fastapi import FastAPI, UploadFile, File, Form
from fastapi.middleware.cors import CORSMiddleware
from typing import Dict
import tempfile
import os

from analysis.frame_extractor import extract_key_frames
from analysis.pose_detector import detect_pose
from analysis.metrics import compute_metrics
from rules.coaching_rules import generate_suggestions

app = FastAPI(title="Tennis Technique Analyzer - Forehand Focus")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def root():
    return {"status": "ok", "message": "Tennis Technique Analyzer backend v2 running"}


@app.post("/analyze")
async def analyze_video(
    file: UploadFile = File(...),
    student_name: str = Form(...),
    stroke_type: str = Form(...)
) -> Dict:
    """Accept a video, run pose analysis, and return coaching feedback."""
    # 1. Save upload to a temporary file
    with tempfile.NamedTemporaryFile(delete=False, suffix=".mp4") as tmp:
        contents = await file.read()
        tmp.write(contents)
        video_path = tmp.name

    # 2. Extract a small set of key frames from the video
    frame_paths = extract_key_frames(video_path, num_frames=6)

    # 3. Run pose detection on each frame
    poses = [detect_pose(p) for p in frame_paths]

    # 4. Compute metrics (currently tuned for forehands)
    metrics = compute_metrics(poses)

    # 5. Generate coaching suggestions based on metrics + stroke type
    suggestions = generate_suggestions(metrics, stroke_type)

    # 6. Cleanup video file (optional: keep frames for debugging UI)
    try:
        os.remove(video_path)
    except OSError:
        pass

    return {
        "student": student_name,
        "stroke": stroke_type,
        "frames": frame_paths,
        "metrics": metrics,
        "suggestions": suggestions,
    }

