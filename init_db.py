import os
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

# Load environment variables from .env file
load_dotenv()

def get_db_url():
    """Get the database URL from environment or use default."""
    db_url = os.getenv("DATABASE_URL")
    if not db_url:
        raise ValueError("DATABASE_URL environment variable is not set")
    return db_url

def get_engine():
    """Create a SQLAlchemy engine."""
    db_url = get_db_url()
    print(f"🔗 Using database: {db_url}")
    return create_engine(db_url, echo=True, future=True)

# Initialize SQLAlchemy engine and Base
engine = get_engine()
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()
