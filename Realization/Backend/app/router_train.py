from fastapi import APIRouter
from app.services.train_service import start_training, get_train_status

router = APIRouter(prefix="/train", tags=["Training"])

@router.post("")
def train(force: bool = False, spark: bool = False):
    return start_training(force=force, use_spark=spark)

@router.get("/status")
def train_status():
    return get_train_status()