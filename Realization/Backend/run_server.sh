#!/bin/bash

echo "Запуск Backend-сервера в venv…"
source venv/bin/activate
uvicorn app.main:app --reload --port 8000