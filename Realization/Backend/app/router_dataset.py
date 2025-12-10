from fastapi import APIRouter, UploadFile, File, HTTPException
from fastapi.responses import JSONResponse
import pandas as pd
import io
import json
import math
from pathlib import Path
from typing import Any

from app.services.model_service import loaded_model

router = APIRouter(prefix="/dataset", tags=["Dataset analysis"])


def sanitize_for_json(obj: Any) -> Any:
    """
    Рекурсивно очищает объект от NaN и Infinity значений для безопасной JSON сериализации
    """
    if isinstance(obj, dict):
        return {k: sanitize_for_json(v) for k, v in obj.items()}
    elif isinstance(obj, list):
        return [sanitize_for_json(item) for item in obj]
    elif isinstance(obj, float):
        if pd.isna(obj) or not math.isfinite(obj):
            return 0.0
        return obj
    elif pd.isna(obj):  # для других типов с NaN
        return None
    return obj


@router.post("/analyze")
async def analyze_dataset(file: UploadFile = File(...)):
    """
    Анализирует датасет отзывов и возвращает статистику по тональности
    
    Args:
        file: CSV, JSON или Parquet файл с колонкой 'review_text'
    
    Returns:
        JSON с результатами анализа
    """
    try:
        # Проверка размера файла (макс 100MB)
        max_size = 100 * 1024 * 1024  # 100MB
        content = await file.read()
        
        if len(content) > max_size:
            raise HTTPException(
                status_code=413,
                detail=f"Файл слишком большой. Максимальный размер: {max_size // (1024*1024)}MB"
            )
        
        # Определение формата файла
        ext = file.filename.split(".")[-1].lower()
        
        # Чтение файла в DataFrame
        try:
            if ext == "csv":
                df = pd.read_csv(io.BytesIO(content), encoding='utf-8')
            elif ext == "json":
                df = pd.read_json(io.BytesIO(content))
            elif ext in ("parquet", "pq"):
                df = pd.read_parquet(io.BytesIO(content))
            else:
                raise HTTPException(
                    status_code=400,
                    detail=f"Неподдерживаемый формат файла: {ext}. Используйте CSV, JSON или Parquet"
                )
        except HTTPException:
            raise
        except Exception as e:
            raise HTTPException(
                status_code=400,
                detail=f"Ошибка чтения файла: {str(e)}"
            )
        
        # Поддержка разных названий колонок с текстом
        text_column = None
        possible_columns = ["clean_text", "review_text", "review", "text", "content"]
        
        for col_name in possible_columns:
            if col_name in df.columns:
                text_column = col_name
                break
        
        if text_column is None:
            available_cols = ", ".join(df.columns.tolist())
            raise HTTPException(
                status_code=400,
                detail=f"Датасет должен содержать одну из колонок: {', '.join(possible_columns)}. Доступные колонки: {available_cols}"
            )
        
        # Проверка модели
        if not loaded_model or not hasattr(loaded_model, 'predict'):
            raise HTTPException(
                status_code=503,
                detail="Модель не загружена. Пожалуйста, обучите модель перед анализом датасета."
            )
        
        # Анализ тональности
        sentiments = []
        for idx, text in enumerate(df[text_column].astype(str).tolist()):
            if pd.isna(text) or text.strip() == "":
                sentiments.append("neutral")  # Для пустых текстов
                continue
            
            try:
                pred = loaded_model.predict(text)
                sentiments.append(pred.get("label", "neutral"))
            except Exception as e:
                print(f"Ошибка при предсказании для текста {idx}: {e}")
                sentiments.append("neutral")  # Fallback
        
        df["sentiment"] = sentiments
        
        # Подсчет статистики
        sentiment_counts = df["sentiment"].value_counts().to_dict()
        
        # Нормализация ключей (приведение к нижнему регистру)
        distribution = {
            "positive": sentiment_counts.get("positive", 0) + sentiment_counts.get("Positive", 0),
            "negative": sentiment_counts.get("negative", 0) + sentiment_counts.get("Negative", 0),
            "neutral": sentiment_counts.get("neutral", 0) + sentiment_counts.get("Neutral", 0)
        }
        
        # Сбор примеров
        examples = {
            "positive": [],
            "neutral": [],
            "negative": []
        }
        
        for sentiment_type in ["positive", "neutral", "negative"]:
            sentiment_df = df[df["sentiment"].str.lower() == sentiment_type]
            if not sentiment_df.empty:
                # Фильтруем NaN и пустые значения из примеров
                example_texts = sentiment_df[text_column].head(10).dropna().astype(str)
                example_texts = [t for t in example_texts.tolist() if t and t.strip() and t != "nan"]
                examples[sentiment_type] = example_texts[:3]  # Берем первые 3 валидных
        
        # Формирование результата
        # Фильтруем пустые строки для вычисления средней длины
        non_empty_texts = df[text_column].dropna().astype(str)
        non_empty_texts = non_empty_texts[non_empty_texts.str.strip() != ""]
        
        avg_length = 0.0
        if len(non_empty_texts) > 0:
            avg_length = float(non_empty_texts.str.len().mean())
            # Проверка на NaN/Infinity
            if pd.isna(avg_length) or not math.isfinite(avg_length):
                avg_length = 0.0
        
        stats = {
            "total_reviews": int(len(df)),
            "distribution": distribution,
            "examples": examples,
            "avg_length": avg_length,
            "detected_column": text_column  # Информируем какую колонку использовали
        }
        
        # Очистка от NaN/Infinity для безопасной сериализации
        stats = sanitize_for_json(stats)
        
        # Сохранение результатов
        logs_dir = Path("logs")
        logs_dir.mkdir(exist_ok=True)
        
        out_path = logs_dir / "dataset_analysis.json"
        with open(out_path, "w", encoding="utf-8") as f:
            json.dump(stats, f, indent=2, ensure_ascii=False)
        
        return JSONResponse(
            status_code=200,
            content={
                "status": "success",
                "analysis": stats,
                "saved_to": str(out_path)
            }
        )
        
    except HTTPException:
        raise
    except Exception as e:
        print(f"Unexpected error in analyze_dataset: {e}")
        raise HTTPException(
            status_code=500,
            detail=f"Внутренняя ошибка сервера: {str(e)}"
        )