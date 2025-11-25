from fastapi import APIRouter, HTTPException
from app.config import MODEL_PATH, VOCAB_PATH
from fastapi.responses import FileResponse

router = APIRouter(tags=["System"])

@router.get("/health")
def health():
    return {
        "model": MODEL_PATH.exists(),
        "vocab": VOCAB_PATH.exists(),
        "status": "ok"
    }

@router.get("/download/model")
def download_model():
    if not MODEL_PATH.exists():
        raise HTTPException(404, "model not found")
    return FileResponse(MODEL_PATH)

@router.get("/download/vocab")
def download_vocab():
    if not VOCAB_PATH.exists():
        raise HTTPException(404, "vocab not found")
    return FileResponse(VOCAB_PATH)