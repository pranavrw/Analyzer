"""
SQLAlchemy models and database session management.
Defines User, Dataset, TrainingLog models and helper functions.
"""

from sqlalchemy import Column, Integer, String, DateTime, Text, ForeignKey, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker
from sqlalchemy.sql import func
from datetime import datetime
from passlib.context import CryptContext
from .config.db_config import engine
import logging

# Setup password hashing
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

Base = declarative_base()

class User(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(80), unique=True, nullable=False, index=True)
    password_hash = Column(String(128), nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # Relationships
    datasets = relationship("Dataset", back_populates="user")
    
    def verify_password(self, password: str) -> bool:
        """Verify password against hash."""
        return pwd_context.verify(password, str(self.password_hash))
    
    @staticmethod
    def hash_password(password: str) -> str:
        """Hash password."""
        return pwd_context.hash(password)

class Dataset(Base):
    __tablename__ = "datasets"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    name = Column(String(200), nullable=False)
    s3_path = Column(String(500), nullable=False)
    local_path = Column(String(500))
    status = Column(String(50), default="uploaded")  # uploaded, processed, training, trained
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # Relationships
    user = relationship("User", back_populates="datasets")

class TrainingLog(Base):
    __tablename__ = "training_logs"
    
    id = Column(Integer, primary_key=True, index=True)
    dataset_id = Column(Integer, ForeignKey("datasets.id"), nullable=True)
    message = Column(Text, nullable=False)
    level = Column(String(20), default="INFO")  # INFO, WARNING, ERROR
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    training_run_id = Column(String(100))  # To group related logs
    
    # Relationships
    dataset = relationship("Dataset")

# Database session management
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def get_db():
    """Dependency to get database session."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Helper functions
def create_user(username: str, password: str) -> User:
    """Create a new user."""
    db = SessionLocal()
    try:
        # Check if user already exists
        existing_user = db.query(User).filter(User.username == username).first()
        if existing_user:
            raise ValueError(f"User '{username}' already exists")
        
        # Create new user
        hashed_password = User.hash_password(password)
        user = User(username=username, password_hash=hashed_password)
        db.add(user)
        db.commit()
        db.refresh(user)
        return user
    except Exception as e:
        db.rollback()
        raise
    finally:
        db.close()

def authenticate_user(username: str, password: str) -> User | None:
    """Authenticate user credentials."""
    db = SessionLocal()
    try:
        user = db.query(User).filter(User.username == username).first()
        if not user or not user.verify_password(password):
            return None
        return user
    finally:
        db.close()

def add_dataset_record(user_id: int, name: str, s3_path: str, local_path: str = None, status: str = "uploaded") -> Dataset:
    """Add a dataset record to the database."""
    db = SessionLocal()
    try:
        dataset = Dataset(
            user_id=user_id,
            name=name,
            s3_path=s3_path,
            local_path=local_path,
            status=status
        )
        db.add(dataset)
        db.commit()
        db.refresh(dataset)
        return dataset
    except Exception as e:
        db.rollback()
        raise
    finally:
        db.close()

def list_user_datasets(user_id: int):
    """List all datasets for a user."""
    db = SessionLocal()
    try:
        datasets = db.query(Dataset).filter(Dataset.user_id == user_id).all()
        return datasets
    finally:
        db.close()

def add_training_log(message: str, level: str = "INFO", dataset_id: int | None = None, training_run_id: str | None = None):
    """Add a training log entry."""
    db = SessionLocal()
    try:
        log = TrainingLog(
            message=message,
            level=level,
            dataset_id=dataset_id,
            training_run_id=training_run_id
        )
        db.add(log)
        db.commit()
        return log
    except Exception as e:
        db.rollback()
        logging.error(f"Failed to add training log: {e}")
        raise
    finally:
        db.close()