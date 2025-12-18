#!/usr/bin/env python3
"""
Bootstrap script to create the first admin user.
Run this before testing the API.

Usage:
    python bootstrap_admin.py
"""

import asyncio
import sys
from pathlib import Path

# Add app to path
sys.path.insert(0, str(Path(__file__).parent))

from app.core.db.session import AsyncSessionLocal
from app.core.models.user import User
from app.core.models.enums import UserRole


async def bootstrap_admin():
    """Create the first admin user if it doesn't exist."""
    async with AsyncSessionLocal() as session:
        # Check if admin already exists
        from sqlalchemy import select
        
        result = await session.execute(
            select(User).where(User.email == "admin@example.com")
        )
        existing_admin = result.scalar_one_or_none()
        
        if existing_admin:
            print(f"✅ Admin user already exists!")
            print(f"   ID: {existing_admin.id}")
            print(f"   Email: {existing_admin.email}")
            print(f"   Use X-User-Id: {existing_admin.id} in your API requests")
            return existing_admin.id
        
        # Create new admin user
        admin = User(
            email="admin@example.com",
            first_name="Admin",
            last_name="User",
            role=UserRole.ADMIN,
        )
        session.add(admin)
        await session.commit()
        await session.refresh(admin)
        
        print(f"✅ Admin user created successfully!")
        print(f"   ID: {admin.id}")
        print(f"   Email: {admin.email}")
        print(f"   Role: {admin.role}")
        print(f"\n📝 Use this in your API requests:")
        print(f"   X-User-Id: {admin.id}")
        
        return admin.id


if __name__ == "__main__":
    try:
        admin_id = asyncio.run(bootstrap_admin())
        print(f"\n✅ Bootstrap complete! You can now use X-User-Id: {admin_id}")
    except Exception as e:
        print(f"❌ Error: {e}")
        print("\nMake sure:")
        print("1. Database is running")
        print("2. DATABASE_URL is set in .env file")
        print("3. Migrations have been run (alembic upgrade head)")
        sys.exit(1)

