#!/usr/bin/env python3
"""
Debug tool: lists database tables and schema to verify DB initialization.
"""

import sys
import os
from pathlib import Path

# Add src to path
sys.path.append(str(Path(__file__).parent))

from src.config.db_config import engine, get_db_url
from sqlalchemy import inspect, text

def check_database():
    """Check database connection and list tables."""
    try:
        print("🔍 Checking database connection...")
        import re
        safe_url = re.sub(r"://[^@]+@", "://***@", get_db_url())
        print(f"Database URL: {safe_url}")
        
        # Test connection
        with engine.connect() as conn:
            result = conn.execute(text("SELECT version()"))
            version = result.fetchone()[0]
            print(f"✅ Connected to PostgreSQL: {version}")
        
        # List tables
        inspector = inspect(engine)
        tables = inspector.get_table_names()
        
        print(f"\n📋 Tables in database ({len(tables)}):")
        for table in tables:
            print(f"  - {table}")
            
            # Get columns for each table
            columns = inspector.get_columns(table)
            for col in columns:
                nullable = "NULL" if col['nullable'] else "NOT NULL"
                print(f"    └─ {col['name']}: {col['type']} {nullable}")
        
        if not tables:
            print("  (No tables found)")
            
    except Exception as e:
        print(f"❌ Error checking database: {e}")
        raise

if __name__ == "__main__":
    check_database()