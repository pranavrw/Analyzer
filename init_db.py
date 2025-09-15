from src.user_db import Base, engine

print("🚀 Creating tables in PostgreSQL...")
Base.metadata.create_all(bind=engine)
print("✅ Database initialized successfully.")
from src.user_db import create_db

if __name__ == "__main__":
    create_db()
    print("✅ PostgreSQL Database initialized successfully")
