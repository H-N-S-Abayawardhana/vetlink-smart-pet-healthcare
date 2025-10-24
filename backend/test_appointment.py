#!/usr/bin/env python3
"""
Test script for appointment creation and email functionality
"""

import asyncio
import sys
import os
from datetime import datetime, timedelta

# Add the app directory to the Python path
sys.path.append(os.path.dirname(__file__))

from app.core.database import AsyncSessionLocal
from app.models.user import User, UserRole
from app.models.appointment import Appointment, AppointmentStatus, PaymentStatus
from app.services.email_service import send_appointment_notification_to_vet
from app.core.security import get_password_hash

async def test_database_connection():
    """Test database connection and create test data."""
    print("Testing database connection...")
    
    async with AsyncSessionLocal() as session:
        try:
            # Test basic query
            from sqlalchemy import select
            result = await session.execute(select(User).limit(1))
            users = result.scalars().all()
            print(f"✅ Database connection successful. Found {len(users)} users.")
            return True
        except Exception as e:
            print(f"❌ Database connection failed: {e}")
            return False

async def create_test_users():
    """Create test users if they don't exist."""
    print("Creating test users...")
    
    async with AsyncSessionLocal() as session:
        try:
            # Check if test users exist
            from sqlalchemy import select
            result = await session.execute(select(User).where(User.email == "testuser@example.com"))
            test_user = result.scalar_one_or_none()
            
            if not test_user:
                # Create test user
                test_user = User(
                    username="testuser",
                    email="testuser@example.com",
                    contact_number="1234567890",
                    password_hash=get_password_hash("password123"),
                    user_role=UserRole.USER,
                    is_active=True
                )
                session.add(test_user)
                print("✅ Created test user")
            else:
                print("✅ Test user already exists")
            
            # Check if test veterinarian exists
            result = await session.execute(select(User).where(User.email == "testvet@example.com"))
            test_vet = result.scalar_one_or_none()
            
            if not test_vet:
                # Create test veterinarian
                test_vet = User(
                    username="testvet",
                    email="testvet@example.com",
                    contact_number="0987654321",
                    password_hash=get_password_hash("password123"),
                    user_role=UserRole.VETERINARIAN,
                    is_active=True
                )
                session.add(test_vet)
                print("✅ Created test veterinarian")
            else:
                print("✅ Test veterinarian already exists")
            
            await session.commit()
            return test_user, test_vet
            
        except Exception as e:
            print(f"❌ Error creating test users: {e}")
            await session.rollback()
            return None, None

async def test_appointment_creation():
    """Test appointment creation."""
    print("Testing appointment creation...")
    
    async with AsyncSessionLocal() as session:
        try:
            # Get test users
            from sqlalchemy import select
            result = await session.execute(select(User).where(User.email == "testuser@example.com"))
            test_user = result.scalar_one()
            
            result = await session.execute(select(User).where(User.email == "testvet@example.com"))
            test_vet = result.scalar_one()
            
            # Create test appointment
            tomorrow = (datetime.now() + timedelta(days=1)).strftime("%Y-%m-%d")
            
            appointment = Appointment(
                user_id=test_user.id,
                veterinarian_id=test_vet.id,
                appointment_date=tomorrow,
                appointment_time="10:00:00",
                reason="Test appointment",
                status=AppointmentStatus.PENDING,
                payment_status=PaymentStatus.UNPAID
            )
            
            session.add(appointment)
            await session.commit()
            await session.refresh(appointment)
            
            print(f"✅ Appointment created successfully with ID: {appointment.id}")
            return appointment
            
        except Exception as e:
            print(f"❌ Error creating appointment: {e}")
            await session.rollback()
            return None

async def test_email_service():
    """Test email service."""
    print("Testing email service...")
    
    try:
        # Test email data
        email_data = {
            "appointment_id": 1,
            "user_email": "testuser@example.com",
            "user_name": "Test User",
            "user_contact": "1234567890",
            "veterinarian_email": "testvet@example.com",
            "veterinarian_name": "Test Vet",
            "veterinarian_contact": "0987654321",
            "appointment_date": "2024-01-15",
            "appointment_time": "10:00:00",
            "reason": "Test appointment",
            "status": "pending"
        }
        
        result = await send_appointment_notification_to_vet(email_data)
        
        if result.get("success"):
            print("✅ Email service test successful")
        else:
            print(f"⚠️ Email service test failed: {result.get('error', 'Unknown error')}")
            print("This is expected if email configuration is not set up")
        
        return result.get("success", False)
        
    except Exception as e:
        print(f"❌ Email service test error: {e}")
        return False

async def main():
    """Run all tests."""
    print("🧪 Starting VetLink Backend Tests\n")
    
    # Test 1: Database connection
    db_ok = await test_database_connection()
    if not db_ok:
        print("❌ Database tests failed. Please check your database configuration.")
        return
    
    print()
    
    # Test 2: Create test users
    test_user, test_vet = await create_test_users()
    if not test_user or not test_vet:
        print("❌ User creation tests failed.")
        return
    
    print()
    
    # Test 3: Create appointment
    appointment = await test_appointment_creation()
    if not appointment:
        print("❌ Appointment creation test failed.")
        return
    
    print()
    
    # Test 4: Email service
    email_ok = await test_email_service()
    
    print()
    print("🎉 Test Summary:")
    print(f"✅ Database connection: {'PASS' if db_ok else 'FAIL'}")
    print(f"✅ User creation: {'PASS' if test_user and test_vet else 'FAIL'}")
    print(f"✅ Appointment creation: {'PASS' if appointment else 'FAIL'}")
    print(f"{'✅' if email_ok else '⚠️'} Email service: {'PASS' if email_ok else 'FAIL (expected if not configured)'}")
    
    if db_ok and test_user and test_vet and appointment:
        print("\n🎉 Core functionality is working! Your appointment system should be functional.")
        if not email_ok:
            print("📧 To enable email notifications, configure your SMTP settings in the .env file.")
    else:
        print("\n❌ Some tests failed. Please check the error messages above.")

if __name__ == "__main__":
    asyncio.run(main())

