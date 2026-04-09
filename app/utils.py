import os
import uuid
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
UPLOAD_DIR = BASE_DIR / "uploads"
PROCESSED_DIR = BASE_DIR / "processed"
TRANSCRIPT_DIR = BASE_DIR / "transcripts"

def init_directories():
    """Initialize necessary directories for storage."""
    for directory in [UPLOAD_DIR, PROCESSED_DIR, TRANSCRIPT_DIR]:
        directory.mkdir(parents=True, exist_ok=True)

def generate_job_id() -> str:
    """Generate a unique job identifier."""
    return str(uuid.uuid4())

def get_upload_path(filename: str) -> Path:
    """Get the path for an uploaded audio file."""
    return UPLOAD_DIR / filename

def get_processed_path(job_id: str) -> Path:
    """Get the path for a processed WAV file."""
    return PROCESSED_DIR / f"{job_id}.wav"

def get_transcript_path(job_id: str) -> Path:
    """Get the path for a transcript JSON file."""
    return TRANSCRIPT_DIR / f"{job_id}.json"
