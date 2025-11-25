from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .router_predict import router as predict_router
from .router_train import router as train_router
from .router_system import router as system_router

app = FastAPI(title="Sentiment Backend", version="1.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Роуты
app.include_router(system_router)
app.include_router(predict_router)
app.include_router(train_router)

@app.get("/")
def root():
    return {"status": "backend running"}