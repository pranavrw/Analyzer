from sqlalchemy import text
from src.user_db import engine

with engine.connect() as conn:
    result = conn.execute(text("SELECT table_name FROM information_schema.tables WHERE table_schema='public';"))
    print("📌 Listing all tables in database:")
    for row in result:
        print(row[0])
