import subprocess
import os
import json
from pathlib import Path
from typing import Dict, Any, List
from faster_whisper import WhisperModel
from .utils import get_processed_path, get_transcript_path

class AudioProcessor:
    @staticmethod
    def normalize(input_path: Path, output_path: Path):
        """
        Normalize audio to 16kHz, mono, WAV format using FFmpeg.
        """
        command = [
            "ffmpeg",
            "-y",  # Overwrite output file if it exists
            "-i", str(input_path),
            "-ar", "16000",
            "-ac", "1",
            "-c:a", "pcm_s16le",
            str(output_path)
        ]
        
        try:
            result = subprocess.run(command, capture_output=True, text=True, check=True)
        except subprocess.CalledProcessError as e:
            raise RuntimeError(f"FFmpeg normalization failed: {e.stderr}")

class TranscriptionEngine:
    def __init__(self, model_size: str = "base", device: str = "cpu", compute_type: str = "int8"):
        # We initialize the model here. In a production app, this might be a singleton.
        self.model = WhisperModel(model_size, device=device, compute_type=compute_type)

    def transcribe(self, audio_path: Path) -> Dict[str, Any]:
        """
        Transcribe audio file and return text and segments.
        Uses VAD filter and generator for low memory usage.
        """
        segments_gen, info = self.model.transcribe(
            str(audio_path),
            beam_size=5,
            vad_filter=True,
            vad_parameters=dict(min_silence_duration_ms=500)
        )

        full_text = []
        segments_list = []

        for segment in segments_gen:
            segment_data = {
                "start": round(segment.start, 2),
                "end": round(segment.end, 2),
                "text": segment.text.strip()
            }
            segments_list.append(segment_data)
            full_text.append(segment.text.strip())

        return {
            "text": " ".join(full_text),
            "segments": segments_list,
            "language": info.language,
            "duration": info.duration
        }

def process_and_transcribe(job_id: str, input_path: Path):
    """
    Main background task: Normalize -> Transcribe -> Save.
    """
    processed_path = get_processed_path(job_id)
    transcript_path = get_transcript_path(job_id)
    
    try:
        AudioProcessor.normalize(input_path, processed_path)
        engine = TranscriptionEngine()
        result = engine.transcribe(processed_path)
        with open(transcript_path, "w", encoding="utf-8") as f:
            json.dump(result, f, indent=2)
            
        return "completed"
    except Exception as e:
        print(f"Error processing job {job_id}: {str(e)}")
        return "failed"
    finally:
        if input_path.exists():
            input_path.unlink()
        if processed_path.exists():
            processed_path.unlink()
