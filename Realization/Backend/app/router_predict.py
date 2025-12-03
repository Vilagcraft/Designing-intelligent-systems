from fastapi import APIRouter, HTTPException
from app.models.predict_request import PredictRequest, BatchRequest
from app.services.model_service import loaded_model

router = APIRouter(prefix="/predict", tags=["Predict"])

@router.post("")
async def predict(req: PredictRequest):
    try:
        return loaded_model.predict(req.text)
    except Exception as e:
        raise HTTPException(500, str(e))

@router.post("/batch")
async def predict_batch(req: BatchRequest):
    results = []
    for text in req.texts:
        try:
            result = loaded_model.predict(text)
            # Возвращаем полные данные включая probs для визуализации
            results.append({
                "text": text, 
                "label": result.get("label"),
                "probs": result.get("probs", []),
                "ok": result.get("ok", True)
            })
        except Exception as e:
            results.append({"text": text, "error": str(e)})
    return {"results": results}