from pydantic import BaseModel
from typing import List

class PredictRequest(BaseModel):
    text: str

class BatchRequest(BaseModel):
    texts: List[str]