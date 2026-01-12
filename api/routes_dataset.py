"""
Dataset management endpoints.
Handles dataset upload, listing, and management.
"""

from fastapi import APIRouter, HTTPException, Depends, UploadFile, File, Form
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from pydantic import BaseModel
from typing import List
import os
import sys
import logging
import shutil
from pathlib import Path

# Add src to path for imports
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from src.user_db import add_dataset_record, list_user_datasets, SessionLocal, User
from src.s3_utils import upload_to_s3
from api.auth import verify_token

router = APIRouter()
logger = logging.getLogger(__name__)

class DatasetResponse(BaseModel):
    id: int
    name: str
    status: str
    created_at: str
    s3_path: str

def get_user_by_username(username: str) -> User:
    """Get user by username."""
    db = SessionLocal()
    try:
        user = db.query(User).filter(User.username == username).first()
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        return user
    finally:
        db.close()

@router.post("/upload")
async def upload_dataset(
    file: UploadFile = File(...),
    dataset_name: str = Form(...),
    username: str = Depends(verify_token)
):
    """Upload a dataset ZIP file."""
    try:
        # Validate file type
        if not file.filename.endswith('.zip'):
            raise HTTPException(status_code=400, detail="Only ZIP files are allowed")
        
        # Get user
        user = get_user_by_username(username)
        
        # Create directories
        raw_dir = Path("data/raw")
        raw_dir.mkdir(parents=True, exist_ok=True)
        
        # Save file locally
        file_path = raw_dir / f"{user.id}_{dataset_name}_{file.filename}"
        
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
        
        # Upload to S3 (if configured)
        s3_key = f"datasets/{user.id}/{dataset_name}/{file.filename}"
        try:
            upload_success = upload_to_s3(str(file_path), s3_key)
            if upload_success:
                logger.info(f"Successfully uploaded dataset to S3: {s3_key}")
                s3_path = s3_key
                upload_status = "uploaded_to_s3"
            else:
                logger.warning(f"S3 upload failed (returned False), storing locally only")
                s3_path = f"local://{file_path}"
                upload_status = "uploaded_local_only"
        except Exception as e:
            logger.warning(f"S3 upload failed with exception: {e}, storing locally only")
            s3_path = f"local://{file_path}"
            upload_status = "uploaded_local_only"
        
        # Add dataset record to database with status
        dataset = add_dataset_record(
            user_id=int(user.id),
            name=dataset_name,
            s3_path=s3_path,
            local_path=str(file_path),
            status=upload_status
        )
        
        return {
            "message": "Dataset uploaded successfully",
            "dataset_id": dataset.id,
            "name": dataset.name,
            "s3_path": dataset.s3_path,
            "status": upload_status,
            "stored_locally": upload_status == "uploaded_local_only"
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error uploading dataset: {e}")
        raise HTTPException(status_code=500, detail="Error uploading dataset")

@router.get("/", response_model=List[DatasetResponse])
async def list_datasets(username: str = Depends(verify_token)):
    """List all datasets for the current user."""
    try:
        # Get user
        user = get_user_by_username(username)
        
        # Get user's datasets
        datasets = list_user_datasets(int(user.id))
        
        return [
            DatasetResponse(
                id=int(dataset.id),
                name=str(dataset.name),
                status=str(dataset.status),
                created_at=dataset.created_at.isoformat(),
                s3_path=str(dataset.s3_path)
            )
            for dataset in datasets
        ]
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error listing datasets: {e}")
        raise HTTPException(status_code=500, detail="Error listing datasets")

@router.get("/{dataset_id}")
async def get_dataset(dataset_id: int, username: str = Depends(verify_token)):
    """Get specific dataset information."""
    try:
        # Get user
        user = get_user_by_username(username)
        
        # Get dataset
        db = SessionLocal()
        try:
            from src.user_db import Dataset
            dataset = db.query(Dataset).filter(
                Dataset.id == dataset_id,
                Dataset.user_id == user.id
            ).first()
            
            if not dataset:
                raise HTTPException(status_code=404, detail="Dataset not found")
            
            return DatasetResponse(
                id=int(dataset.id),
                name=str(dataset.name),
                status=str(dataset.status),
                created_at=dataset.created_at.isoformat(),
                s3_path=str(dataset.s3_path)
            )
        finally:
            db.close()
            
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error getting dataset: {e}")
        raise HTTPException(status_code=500, detail="Error getting dataset")