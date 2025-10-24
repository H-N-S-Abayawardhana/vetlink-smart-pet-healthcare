from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func, and_
from sqlalchemy.orm import selectinload
from typing import Optional
from datetime import datetime

from app.core.database import get_db
from app.models.user import User, UserRole
from app.models.appointment import Appointment, AppointmentStatus
from app.api.v1.endpoints.auth import get_current_user

router = APIRouter()

@router.get("/")
async def get_veterinarians(
    date: Optional[str] = Query(None),
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Get list of available veterinarians."""
    
    # Only USER role can view veterinarians for appointment scheduling
    if current_user.user_role != UserRole.USER:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Access denied. Only users can view veterinarians."
        )
    
    # Use provided date or default to today
    target_date = date or datetime.now().strftime("%Y-%m-%d")
    
    # Get veterinarians with appointment counts for the date
    query = select(
        User.id,
        User.username,
        User.email,
        User.contact_number,
        User.created_at,
        func.count(Appointment.id).label("total_appointments"),
        func.count(
            func.case(
                (Appointment.status == AppointmentStatus.PENDING, 1),
                else_=None
            )
        ).label("pending_appointments"),
        func.count(
            func.case(
                (Appointment.status == AppointmentStatus.ACCEPTED, 1),
                else_=None
            )
        ).label("accepted_appointments")
    ).select_from(
        User.outerjoin(
            Appointment,
            and_(
                User.id == Appointment.veterinarian_id,
                Appointment.appointment_date == target_date,
                Appointment.status.in_([AppointmentStatus.PENDING, AppointmentStatus.ACCEPTED])
            )
        )
    ).where(
        and_(
            User.user_role == UserRole.VETERINARIAN,
            User.is_active == True
        )
    ).group_by(
        User.id, User.username, User.email, User.contact_number, User.created_at
    ).order_by(User.username)
    
    result = await db.execute(query)
    veterinarians = result.all()
    
    return {
        "success": True,
        "veterinarians": [
            {
                "id": vet.id,
                "username": vet.username,
                "email": vet.email,
                "contact_number": vet.contact_number,
                "created_at": vet.created_at,
                "total_appointments": vet.total_appointments,
                "pending_appointments": vet.pending_appointments,
                "accepted_appointments": vet.accepted_appointments
            }
            for vet in veterinarians
        ]
    }

@router.get("/{veterinarian_id}/availability")
async def get_veterinarian_availability(
    veterinarian_id: int,
    date: str = Query(..., description="Date in YYYY-MM-DD format"),
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Get veterinarian availability for a specific date."""
    
    # Only USER role can check veterinarian availability
    if current_user.user_role != UserRole.USER:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Access denied. Only users can check availability."
        )
    
    # Verify veterinarian exists and is active
    vet_result = await db.execute(
        select(User).where(
            and_(
                User.id == veterinarian_id,
                User.user_role == UserRole.VETERINARIAN,
                User.is_active == True
            )
        )
    )
    veterinarian = vet_result.scalar_one_or_none()
    
    if not veterinarian:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Veterinarian not found"
        )
    
    # Get booked time slots for the date
    booked_result = await db.execute(
        select(Appointment.appointment_time, Appointment.status).where(
            and_(
                Appointment.veterinarian_id == veterinarian_id,
                Appointment.appointment_date == date,
                Appointment.status.in_([AppointmentStatus.PENDING, AppointmentStatus.ACCEPTED])
            )
        ).order_by(Appointment.appointment_time)
    )
    booked_slots = booked_result.all()
    
    # Define available time slots (9 AM to 5 PM, 30-minute intervals)
    available_slots = []
    start_hour = 9
    end_hour = 17
    
    for hour in range(start_hour, end_hour):
        for minute in range(0, 60, 30):
            time_string = f"{hour:02d}:{minute:02d}:00"
            display_time = f"{hour:02d}:{minute:02d}"
            
            # Check if this time slot is booked
            is_booked = any(booking.appointment_time == time_string for booking in booked_slots)
            
            available_slots.append({
                "time": time_string,
                "display_time": display_time,
                "available": not is_booked
            })
    
    return {
        "success": True,
        "veterinarian": {
            "id": veterinarian.id,
            "username": veterinarian.username
        },
        "date": date,
        "available_slots": available_slots,
        "booked_appointments": [
            {
                "appointment_time": booking.appointment_time,
                "status": booking.status
            }
            for booking in booked_slots
        ]
    }

