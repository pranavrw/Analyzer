"""
Central database configuration module.
Builds SQLAlchemy DB_URL from environment variables.
"""

import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv

# Load .env file
BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
ENV_PATH = os.path.join(BASE_DIR, ".env")
load_dotenv(ENV_PATH)

def get_db_url():
    """Get database URL from environment variables."""
    db_url = os.getenv("DATABASE_URL")
    if not db_url:
        raise ValueError("DATABASE_URL environment variable is not set")
    return db_url

def get_engine():
    """Create and return SQLAlchemy engine."""
    db_url = get_db_url()
    engine = create_engine(
        db_url,
        pool_recycle=300,
        pool_pre_ping=True,
        echo=True  # enable logs for debugging
    )
    return engine

def get_session():
    """Create and return database session."""
    engine = get_engine()
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    return SessionLocal()

# Global engine and session factory
engine = get_engine()
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
