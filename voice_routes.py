import os
import tempfile

from fastapi import APIRouter, UploadFile, File, HTTPException
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

router = APIRouter(prefix="/api/voice", tags=["Voice"])

client = OpenAI(
    api_key=os.getenv("OPENAI_API_KEY")
)


@router.post("/transcribe")
async def transcribe_audio(file: UploadFile = File(...)):

    allowed_types = {
        "audio/mpeg",
        "audio/wav",
        "audio/x-wav",
        "audio/webm",
        "audio/ogg",
        "audio/mp4",
        "audio/x-m4a",
        "audio/flac",
    }

    if file.content_type not in allowed_types:
        raise HTTPException(
            status_code=400,
            detail="Unsupported audio format"
        )

    temp_path = None

    try:
        audio_data = await file.read()

        suffix = os.path.splitext(file.filename or "")[1]

        with tempfile.NamedTemporaryFile(
            delete=False,
            suffix=suffix
        ) as temp_file:

            temp_file.write(audio_data)
            temp_path = temp_file.name

        with open(temp_path, "rb") as audio_file:

            transcription = client.audio.transcriptions.create(
                model="gpt-4o-mini-transcribe",
                file=audio_file
            )

        return {
            "success": True,
            "text": transcription.text
        }

    except Exception as e:

        raise HTTPException(
            status_code=500,
            detail=f"Transcription failed: {str(e)}"
        )

    finally:

        if temp_path and os.path.exists(temp_path):
            os.remove(temp_path)