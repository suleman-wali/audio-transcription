import os
import json
from fastapi import FastAPI, UploadFile, File, BackgroundTasks, HTTPException
from typing import Dict, Any
from .utils import (
    init_directories, 
    generate_job_id, 
    get_upload_path, 
    get_transcript_path
)
from .transcription_engine import process_and_transcribe

app = FastAPI(title="Audio Transcription Pipeline")

JOBS: Dict[str, str] = {}

@app.on_event("startup")
async def startup_event():
    init_directories()

async def run_transcription_task(job_id: str, file_path: os.PathLike):
    JOBS[job_id] = "processing"
    status = process_and_transcribe(job_id, file_path)
    JOBS[job_id] = status

@app.post("/upload")
async def upload_audio(background_tasks: BackgroundTasks, file: UploadFile = File(...)):
    # Validate file extension
    allowed_extensions = {".mp3", ".wav", ".m4a", ".flac", ".ogg"}
    file_ext = os.path.splitext(file.filename)[1].lower()
    if file_ext not in allowed_extensions:
        raise HTTPException(status_code=400, detail="Unsupported file format")

    job_id = generate_job_id()
    file_path = get_upload_path(f"{job_id}{file_ext}")
    
    # Save uploaded file
    try:
        with open(file_path, "wb") as f:
            f.write(await file.read())
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to save file: {str(e)}")

    JOBS[job_id] = "pending"
    
    # Add background task
    background_tasks.add_task(run_transcription_task, job_id, file_path)
    
    return {"job_id": job_id, "status": "pending"}

@app.get("/status/{job_id}")
async def get_status(job_id: str):
    if job_id not in JOBS:
        raise HTTPException(status_code=404, detail="Job not found")
    
    return {"job_id": job_id, "status": JOBS[job_id]}

@app.get("/transcript/{job_id}")
async def get_transcript(job_id: str):
    if job_id not in JOBS:
        raise HTTPException(status_code=404, detail="Job not found")
    
    status = JOBS[job_id]
    if status == "pending" or status == "processing":
        return {"job_id": job_id, "status": status, "message": "Transcript is not ready yet"}
    
    if status == "failed":
        return {"job_id": job_id, "status": status, "message": "Transcription failed"}

    transcript_path = get_transcript_path(job_id)
    if not transcript_path.exists():
        raise HTTPException(status_code=500, detail="Transcript file missing despite completed status")

    with open(transcript_path, "r", encoding="utf-8") as f:
        result = json.load(f)
    
    return result

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
