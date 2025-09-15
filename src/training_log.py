import sqlite3
from datetime import datetime

DB = "users.db"

def _conn():
    return sqlite3.connect(DB)

def log_training(success: bool, details: str):
    conn = _conn()
    cur = conn.cursor()
    cur.execute("INSERT INTO training_logs (timestamp, success, details) VALUES (?, ?, ?)",
                (datetime.utcnow().isoformat(), 1 if success else 0, details))
    conn.commit()
    conn.close()

def get_training_logs(limit=50):
    conn = _conn()
    cur = conn.cursor()
    cur.execute("SELECT id, timestamp, success, details FROM training_logs ORDER BY id DESC LIMIT ?", (limit,))
    rows = cur.fetchall()
    conn.close()
    return [dict(id=r[0], timestamp=r[1], success=bool(r[2]), details=r[3]) for r in rows]
