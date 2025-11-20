# Tennis Technique Analyzer

Monorepo for a simple tennis video analysis app.

## Structure

- `backend/` – FastAPI service that:
  - accepts a video upload
  - extracts a few frames
  - runs pose estimation (placeholder ready)
  - computes basic metrics
  - returns coaching suggestions

- `frontend/` – React web app that:
  - lets you enter student name & stroke type
  - upload a video
  - sends it to the backend
  - shows "What you're doing well" and "What to improve"

This repo is designed so you can:

- Run the backend on your MacBook
- Open the frontend from your Android phone
- Later deploy both to the cloud
- Later add pro comparison, saving analyses, etc.
