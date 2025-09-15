# test_db_insert.py
from src.user_db import SessionLocal, User

db = SessionLocal()
new_user = User(username="testuser", password="1234")
db.add(new_user)
db.commit()
print("✅ Inserted user with ID:", new_user.id)
db.close()
