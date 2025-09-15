from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import List  # ✅ for Python 3.8
from src.user_db import add_dataset_record, list_user_datasets

router = APIRouter()

class DatasetUploadRequest(BaseModel):
    user_id: int
    dataset_name: str
    labels: List[str]  # ✅ instead of list[str]


@router.post("/dataset/upload")
def upload_dataset(request: DatasetUploadRequest):
    try:
        dataset = add_dataset_record(request.user_id, request.dataset_name, request.labels)
        return {"message": "✅ Dataset uploaded successfully", "dataset": dataset}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


class DatasetListRequest(BaseModel):
    user_id: int


@router.post("/dataset/list")
def list_datasets(request: DatasetListRequest):
    datasets = list_user_datasets(request.user_id)
    return {"datasets": datasets}
