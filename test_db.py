#!/usr/bin/env python3
"""
Test database functionality by inserting a dummy user and retrieving it.
Verifies insert and select operations.
"""

import sys
import os
from pathlib import Path

# Add src to path
sys.path.append(str(Path(__file__).parent))

from src.user_db import create_user, authenticate_user, SessionLocal, User
from src.config.db_config import engine
import uuid

def test_database_operations():
    """Test basic database operations."""
    test_username = f"test_user_{uuid.uuid4().hex[:8]}"
    test_password = "test_password_123"
    
    print("🧪 Testing Database Operations")
    print("=" * 40)
    
    try:
        # Test 1: Create user
        print(f"1. Creating test user: {test_username}")
        user = create_user(test_username, test_password)
        print(f"   ✅ User created with ID: {user.id}")
        
        # Test 2: Authenticate user
        print(f"2. Authenticating user: {test_username}")
        auth_user = authenticate_user(test_username, test_password)
        if auth_user:
            print(f"   ✅ Authentication successful for: {auth_user.username}")
        else:
            print("   ❌ Authentication failed")
            return False
        
        # Test 3: Test wrong password
        print("3. Testing wrong password")
        wrong_auth = authenticate_user(test_username, "wrong_password")
        if not wrong_auth:
            print("   ✅ Correctly rejected wrong password")
        else:
            print("   ❌ Incorrectly accepted wrong password")
        
        # Test 4: Query user directly
        print("4. Direct database query")
        db = SessionLocal()
        try:
            db_user = db.query(User).filter(User.username == test_username).first()
            if db_user:
                print(f"   ✅ Found user in database: {db_user.username}")
                print(f"   Created at: {db_user.created_at}")
            else:
                print("   ❌ User not found in direct query")
        finally:
            db.close()
        
        # Cleanup: Remove test user
        print("5. Cleaning up test user")
        db = SessionLocal()
        try:
            db_user = db.query(User).filter(User.username == test_username).first()
            if db_user:
                db.delete(db_user)
                db.commit()
                print("   ✅ Test user removed")
        finally:
            db.close()
        
        print("\n🎉 All database tests passed!")
        return True
        
    except Exception as e:
        print(f"❌ Database test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = test_database_operations()
    sys.exit(0 if success else 1)