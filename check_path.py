#!/usr/bin/env python3
"""
Prints database connection string to confirm correct environment.
"""

import os
import sys
from pathlib import Path

# Add src to path
sys.path.append(str(Path(__file__).parent))

from src.config.db_config import get_db_url

def check_environment():
    """Check and display environment configuration."""
    print("🔧 Environment Configuration Check")
    print("=" * 40)
    
    # Database URL
    try:
        db_url = get_db_url()
        # Hide password for security
        import re
        safe_url = re.sub(r"://[^@]+@", "://***@", db_url) if '://' in db_url else db_url
        print(f"DATABASE_URL: {safe_url}")
    except Exception as e:
        print(f"❌ DATABASE_URL error: {e}")
    
    # Other environment variables
    env_vars = [
        'PGHOST', 'PGPORT', 'PGUSER', 'PGDATABASE',
        'SESSION_SECRET', 'S3_BUCKET_NAME'
    ]
    
    print("\n📋 Environment Variables:")
    for var in env_vars:
        value = os.getenv(var)
        if value:
            # Hide sensitive values
            if 'SECRET' in var or 'PASSWORD' in var:
                display_value = "***"
            else:
                display_value = value
            print(f"  {var}: {display_value}")
        else:
            print(f"  {var}: (not set)")
    
    # Check directories
    print("\n📁 Directory Structure:")
    dirs_to_check = ['data/raw', 'data/processed', 'models', 'config']
    for dir_path in dirs_to_check:
        path = Path(dir_path)
        if path.exists():
            print(f"  {dir_path}: ✅ exists")
        else:
            print(f"  {dir_path}: ❌ missing")

if __name__ == "__main__":
    check_environment()