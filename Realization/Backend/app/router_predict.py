from fastapi import APIRouter, HTTPException

from Realization.Backend.app.models.predict_request import PredictRequest, BatchRequest
from Realization.Backend.app.services.model_service import loaded_model

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
            results.append({"text": text, "label": result["label"]})
        except Exception as e:
            results.append({"text": text, "error": str(e)})
    return {"results": results}