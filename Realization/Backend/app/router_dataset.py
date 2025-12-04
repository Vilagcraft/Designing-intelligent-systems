from fastapi import APIRouter, UploadFile, File
import pandas as pd
import io
import json

from Realization.Backend.app.services.model_service import loaded_model

router = APIRouter(prefix="/dataset", tags=["Dataset analysis"])


@router.post("/analyze")
async def analyze_dataset(file: UploadFile = File(...)):
    ext = file.filename.split(".")[-1].lower()

    content = await file.read()

    if ext == "csv":
        df = pd.read_csv(io.BytesIO(content))
    elif ext == "json":
        df = pd.read_json(io.BytesIO(content))
    elif ext in ("parquet", "pq"):
        df = pd.read_parquet(io.BytesIO(content))
    else:
        return {"error": f"Unsupported file format: {ext}"}

    if "review_text" not in df.columns:
        return {"error": "Dataset must contain column 'review_text'"}

    sentiments = []
    for text in df["review_text"].astype(str).tolist():
        pred = loaded_model.predict(text)["label"]
        sentiments.append(pred)

    df["sentiment"] = sentiments

    stats = {
        "total_reviews": len(df),
        "distribution": df["sentiment"].value_counts().to_dict(),
        "examples": {
            "positive": df[df["sentiment"] == "positive"]["review_text"].head(3).tolist(),
            "neutral": df[df["sentiment"] == "neutral"]["review_text"].head(3).tolist(),
            "negative": df[df["sentiment"] == "negative"]["review_text"].head(3).tolist(),
        },
        "avg_length": float(df["review_text"].str.len().mean())
    }

    out_path = "logs/dataset_analysis.json"
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(stats, f, indent=2, ensure_ascii=False)

    return {
        "status": "success",
        "analysis": stats,
        "saved_to": out_path
    }