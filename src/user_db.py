# src/user_db.py
import datetime
from typing import Generator, List

from sqlalchemy import (
    Column, Integer, String, ForeignKey, DateTime, create_engine
)
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship, Session

from src.config.db_config import DB_URL

# SQLAlchemy setup
engine = create_engine(DB_URL, echo=False, future=True)
SessionLocal = sessionmaker(bind=engine, autocommit=False, autoflush=False)
Base = declarative_base()

# Models
class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, nullable=False, index=True)
    password = Column(String, nullable=False)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)

    datasets = relationship("Dataset", back_populates="owner")


class Dataset(Base):
    __tablename__ = "datasets"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    filename = Column(String, nullable=False)
    s3_key = Column(String, nullable=False)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)

    owner = relationship("User", back_populates="datasets")


class TrainingLog(Base):
    __tablename__ = "training_logs"
    id = Column(Integer, primary_key=True, index=True)
    message = Column(String, nullable=False)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)


# DB helpers
def create_db() -> None:
    """Create all tables (call this once)."""
    Base.metadata.create_all(bind=engine)


def get_db() -> Generator[Session, None, None]:
    """Yield a DB session and ensure close after use (for FastAPI dependency)."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# Simple CRUD helpers (use inside routes with injected session)
def create_user(db: Session, username: str, password: str):
    user = User(username=username, password=password)
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


def authenticate_user(db: Session, username: str, password: str):
    # if using hashed passwords, verify here (example expects raw pw)
    user = db.query(User).filter(User.username == username).first()
    if user and user.password == password:
        return user
    return None


def add_dataset_record(db: Session, user_id: int, filename: str, s3_key: str):
    ds = Dataset(user_id=user_id, filename=filename, s3_key=s3_key)
    db.add(ds)
    db.commit()
    db.refresh(ds)
    return ds


def list_user_datasets(db: Session, user_id: int) -> List[Dataset]:
    return db.query(Dataset).filter(Dataset.user_id == user_id).all()
