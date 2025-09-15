from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from src.training_log import get_training_logs

router = APIRouter()

class AnalyzerRequest(BaseModel):
    user_id: int

@router.post("/analyzer/logs")
def analyzer_logs(request: AnalyzerRequest):
    try:
        logs = get_training_logs(request.user_id)
        return {"logs": logs}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
