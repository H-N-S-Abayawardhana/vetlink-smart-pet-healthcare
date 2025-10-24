from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, and_, or_, func
from sqlalchemy.orm import selectinload
from typing import Optional, List
from datetime import datetime, timedelta

from app.core.database import get_db
from app.models.user import User, UserRole
from app.models.appointment import Appointment, AppointmentStatus, PaymentStatus
from app.schemas.appointment import (
    AppointmentCreate, AppointmentUpdate, AppointmentResponse, 
    AppointmentListResponse, PaymentRequest, PaymentResponse
)
from app.api.v1.endpoints.auth import get_current_user
from app.services.email_service import send_appointment_notification_to_vet, send_appointment_status_to_user

router = APIRouter()

@router.get("/", response_model=AppointmentListResponse)
async def get_appointments(
    status: Optional[AppointmentStatus] = Query(None),
    veterinarian_id: Optional[int] = Query(None),
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Get appointments based on user role and filters."""
    
    # Build base query
    query = select(Appointment).options(
        selectinload(Appointment.user),
        selectinload(Appointment.veterinarian)
    )
    
    # Apply role-based filtering
    if current_user.user_role == UserRole.USER:
        query = query.where(Appointment.user_id == current_user.id)
    elif current_user.user_role == UserRole.VETERINARIAN:
        query = query.where(Appointment.veterinarian_id == current_user.id)
    # SUPER_ADMIN can see all appointments
    
    # Apply additional filters
    conditions = []
    if status:
        conditions.append(Appointment.status == status)
    if veterinarian_id:
        conditions.append(Appointment.veterinarian_id == veterinarian_id)
    
    if conditions:
        query = query.where(and_(*conditions))
    
    # Order by date and time
    query = query.order_by(Appointment.appointment_date.desc(), Appointment.appointment_time.desc())
    
    result = await db.execute(query)
    appointments = result.scalars().all()
    
    # Convert to response format
    appointment_responses = []
    for appointment in appointments:
        appointment_data = {
            "id": appointment.id,
            "user_id": appointment.user_id,
            "veterinarian_id": appointment.veterinarian_id,
            "appointment_date": appointment.appointment_date,
            "appointment_time": appointment.appointment_time,
            "reason": appointment.reason,
            "status": appointment.status,
            "reschedule_reason": appointment.reschedule_reason,
            "rescheduled_from": appointment.rescheduled_from,
            "payment_status": appointment.payment_status,
            "created_at": appointment.created_at,
            "updated_at": appointment.updated_at,
            "confirmed_at": appointment.confirmed_at,
            "completed_at": appointment.completed_at,
            "user_name": appointment.user.username,
            "user_email": appointment.user.email,
            "user_contact": appointment.user.contact_number,
            "veterinarian_name": appointment.veterinarian.username,
            "veterinarian_email": appointment.veterinarian.email,
            "veterinarian_contact": appointment.veterinarian.contact_number,
        }
        appointment_responses.append(AppointmentResponse(**appointment_data))
    
    return AppointmentListResponse(appointments=appointment_responses, total=len(appointment_responses))

@router.post("/", response_model=AppointmentResponse)
async def create_appointment(
    appointment_data: AppointmentCreate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Create a new appointment."""
    
    # Only USER role can create appointments
    if current_user.user_role != UserRole.USER:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only users can schedule appointments"
        )
    
    # Validate appointment date is not in the past
    appointment_datetime = datetime.strptime(f"{appointment_data.appointment_date}T{appointment_data.appointment_time}", "%Y-%m-%dT%H:%M:%S")
    if appointment_datetime < datetime.now():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Cannot schedule appointments in the past"
        )
    
    # Verify veterinarian exists and is active
    vet_result = await db.execute(
        select(User).where(
            and_(
                User.id == appointment_data.veterinarian_id,
                User.user_role == UserRole.VETERINARIAN,
                User.is_active == True
            )
        )
    )
    veterinarian = vet_result.scalar_one_or_none()
    
    if not veterinarian:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid veterinarian selected"
        )
    
    # Check for conflicting appointments
    conflict_result = await db.execute(
        select(Appointment).where(
            and_(
                Appointment.veterinarian_id == appointment_data.veterinarian_id,
                Appointment.appointment_date == appointment_data.appointment_date,
                Appointment.appointment_time == appointment_data.appointment_time,
                Appointment.status.in_([AppointmentStatus.PENDING, AppointmentStatus.ACCEPTED])
            )
        )
    )
    
    if conflict_result.scalar_one_or_none():
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="This time slot is already booked"
        )
    
    # Create the appointment
    db_appointment = Appointment(
        user_id=current_user.id,
        veterinarian_id=appointment_data.veterinarian_id,
        appointment_date=appointment_data.appointment_date,
        appointment_time=appointment_data.appointment_time,
        reason=appointment_data.reason,
        status=AppointmentStatus.PENDING,
        payment_status=PaymentStatus.UNPAID
    )
    
    db.add(db_appointment)
    await db.commit()
    await db.refresh(db_appointment)
    
    # Send email notification to veterinarian
    try:
        email_result = await send_appointment_notification_to_vet({
            "appointment_id": db_appointment.id,
            "user_email": current_user.email,
            "user_name": current_user.username,
            "user_contact": current_user.contact_number,
            "veterinarian_email": veterinarian.email,
            "veterinarian_name": veterinarian.username,
            "veterinarian_contact": veterinarian.contact_number,
            "appointment_date": appointment_data.appointment_date,
            "appointment_time": appointment_data.appointment_time,
            "reason": appointment_data.reason,
            "status": "pending"
        })
        if not email_result.get("success"):
            print(f"Email notification failed: {email_result.get('error', 'Unknown error')}")
    except Exception as email_error:
        print(f"Failed to send email notification to veterinarian: {email_error}")
        # Don't fail the appointment creation if email fails
    
    # Return appointment with user details
    appointment_response = AppointmentResponse(
        id=db_appointment.id,
        user_id=db_appointment.user_id,
        veterinarian_id=db_appointment.veterinarian_id,
        appointment_date=db_appointment.appointment_date,
        appointment_time=db_appointment.appointment_time,
        reason=db_appointment.reason,
        status=db_appointment.status,
        reschedule_reason=db_appointment.reschedule_reason,
        rescheduled_from=db_appointment.rescheduled_from,
        payment_status=db_appointment.payment_status,
        created_at=db_appointment.created_at,
        updated_at=db_appointment.updated_at,
        confirmed_at=db_appointment.confirmed_at,
        completed_at=db_appointment.completed_at,
        user_name=current_user.username,
        user_email=current_user.email,
        user_contact=current_user.contact_number,
        veterinarian_name=veterinarian.username,
        veterinarian_email=veterinarian.email,
        veterinarian_contact=veterinarian.contact_number,
    )
    
    return appointment_response

@router.get("/{appointment_id}", response_model=AppointmentResponse)
async def get_appointment(
    appointment_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Get a specific appointment."""
    
    result = await db.execute(
        select(Appointment).options(
            selectinload(Appointment.user),
            selectinload(Appointment.veterinarian)
        ).where(Appointment.id == appointment_id)
    )
    appointment = result.scalar_one_or_none()
    
    if not appointment:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Appointment not found"
        )
    
    # Check if user has access to this appointment
    has_access = (
        current_user.user_role == UserRole.SUPER_ADMIN or
        (current_user.user_role == UserRole.USER and appointment.user_id == current_user.id) or
        (current_user.user_role == UserRole.VETERINARIAN and appointment.veterinarian_id == current_user.id)
    )
    
    if not has_access:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Access denied"
        )
    
    return AppointmentResponse(
        id=appointment.id,
        user_id=appointment.user_id,
        veterinarian_id=appointment.veterinarian_id,
        appointment_date=appointment.appointment_date,
        appointment_time=appointment.appointment_time,
        reason=appointment.reason,
        status=appointment.status,
        reschedule_reason=appointment.reschedule_reason,
        rescheduled_from=appointment.rescheduled_from,
        payment_status=appointment.payment_status,
        created_at=appointment.created_at,
        updated_at=appointment.updated_at,
        confirmed_at=appointment.confirmed_at,
        completed_at=appointment.completed_at,
        user_name=appointment.user.username,
        user_email=appointment.user.email,
        user_contact=appointment.user.contact_number,
        veterinarian_name=appointment.veterinarian.username,
        veterinarian_email=appointment.veterinarian.email,
        veterinarian_contact=appointment.veterinarian.contact_number,
    )

@router.put("/{appointment_id}", response_model=AppointmentResponse)
async def update_appointment(
    appointment_id: int,
    appointment_update: AppointmentUpdate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Update an appointment."""
    
    # Get current appointment
    result = await db.execute(select(Appointment).where(Appointment.id == appointment_id))
    appointment = result.scalar_one_or_none()
    
    if not appointment:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Appointment not found"
        )
    
    # Check if user has access to update this appointment
    has_access = (
        current_user.user_role == UserRole.SUPER_ADMIN or
        (current_user.user_role == UserRole.USER and appointment.user_id == current_user.id) or
        (current_user.user_role == UserRole.VETERINARIAN and appointment.veterinarian_id == current_user.id)
    )
    
    if not has_access:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Access denied"
        )
    
    # Update fields
    update_data = appointment_update.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(appointment, field, value)
    
    # Set timestamps for status changes
    if appointment_update.status == AppointmentStatus.ACCEPTED:
        appointment.confirmed_at = datetime.utcnow()
    elif appointment_update.status == AppointmentStatus.COMPLETED:
        appointment.completed_at = datetime.utcnow()
    
    await db.commit()
    await db.refresh(appointment)
    
    # Send email notification if status changed
    if appointment_update.status in [AppointmentStatus.ACCEPTED, AppointmentStatus.REJECTED]:
        try:
            # Get user and veterinarian details
            user_result = await db.execute(select(User).where(User.id == appointment.user_id))
            vet_result = await db.execute(select(User).where(User.id == appointment.veterinarian_id))
            user = user_result.scalar_one()
            veterinarian = vet_result.scalar_one()
            
            email_result = await send_appointment_status_to_user({
                "appointment_id": appointment.id,
                "user_email": user.email,
                "user_name": user.username,
                "user_contact": user.contact_number,
                "veterinarian_email": veterinarian.email,
                "veterinarian_name": veterinarian.username,
                "veterinarian_contact": veterinarian.contact_number,
                "appointment_date": appointment.appointment_date,
                "appointment_time": appointment.appointment_time,
                "reason": appointment.reason,
                "status": appointment_update.status.value
            })
            if not email_result.get("success"):
                print(f"Email notification failed: {email_result.get('error', 'Unknown error')}")
        except Exception as email_error:
            print(f"Failed to send email notification to user: {email_error}")
    
    # Return updated appointment
    user_result = await db.execute(select(User).where(User.id == appointment.user_id))
    vet_result = await db.execute(select(User).where(User.id == appointment.veterinarian_id))
    user = user_result.scalar_one()
    veterinarian = vet_result.scalar_one()
    
    return AppointmentResponse(
        id=appointment.id,
        user_id=appointment.user_id,
        veterinarian_id=appointment.veterinarian_id,
        appointment_date=appointment.appointment_date,
        appointment_time=appointment.appointment_time,
        reason=appointment.reason,
        status=appointment.status,
        reschedule_reason=appointment.reschedule_reason,
        rescheduled_from=appointment.rescheduled_from,
        payment_status=appointment.payment_status,
        created_at=appointment.created_at,
        updated_at=appointment.updated_at,
        confirmed_at=appointment.confirmed_at,
        completed_at=appointment.completed_at,
        user_name=user.username,
        user_email=user.email,
        user_contact=user.contact_number,
        veterinarian_name=veterinarian.username,
        veterinarian_email=veterinarian.email,
        veterinarian_contact=veterinarian.contact_number,
    )

@router.delete("/{appointment_id}")
async def cancel_appointment(
    appointment_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Cancel an appointment."""
    
    # Get current appointment
    result = await db.execute(select(Appointment).where(Appointment.id == appointment_id))
    appointment = result.scalar_one_or_none()
    
    if not appointment:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Appointment not found"
        )
    
    # Check if user has access to cancel this appointment
    has_access = (
        current_user.user_role == UserRole.SUPER_ADMIN or
        (current_user.user_role == UserRole.USER and appointment.user_id == current_user.id) or
        (current_user.user_role == UserRole.VETERINARIAN and appointment.veterinarian_id == current_user.id)
    )
    
    if not has_access:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Access denied"
        )
    
    # Update status to cancelled
    appointment.status = AppointmentStatus.CANCELLED
    await db.commit()
    
    return {"message": "Appointment cancelled successfully"}

@router.post("/{appointment_id}/payment", response_model=PaymentResponse)
async def process_payment(
    appointment_id: int,
    payment_data: PaymentRequest,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Process payment for an appointment."""
    
    # Only USER role can make payments
    if current_user.user_role != UserRole.USER:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only users can make payments"
        )
    
    # Get appointment
    result = await db.execute(
        select(Appointment).options(
            selectinload(Appointment.user),
            selectinload(Appointment.veterinarian)
        ).where(Appointment.id == appointment_id)
    )
    appointment = result.scalar_one_or_none()
    
    if not appointment:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Appointment not found"
        )
    
    # Check if user owns this appointment
    if appointment.user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Access denied"
        )
    
    # Check if appointment is accepted
    if appointment.status != AppointmentStatus.ACCEPTED:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Payment can only be made for accepted appointments"
        )
    
    # Check if already paid
    if appointment.payment_status == PaymentStatus.PAID:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Appointment is already paid"
        )
    
    # Validate amount (you can set your own pricing logic here)
    expected_amount = 50.0  # Default consultation fee
    if payment_data.amount != expected_amount:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Invalid amount. Expected ${expected_amount}"
        )
    
    # Simulate payment processing
    payment_result = await process_payment_simulation({
        "appointment_id": appointment_id,
        "amount": payment_data.amount,
        "payment_method": payment_data.payment_method,
        "payment_details": payment_data.payment_details,
        "user_email": appointment.user.email,
        "veterinarian_email": appointment.veterinarian.email
    })
    
    if not payment_result["success"]:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Payment processing failed"
        )
    
    # Update appointment payment status
    appointment.payment_status = PaymentStatus.PAID
    await db.commit()
    
    return PaymentResponse(**payment_result["payment"])

async def process_payment_simulation(payment_data: dict) -> dict:
    """Simulate payment processing."""
    import asyncio
    import uuid
    
    # Simulate payment processing delay
    await asyncio.sleep(1)
    
    # In a real application, you would:
    # 1. Validate payment details
    # 2. Process payment through payment gateway (Stripe, PayPal, etc.)
    # 3. Handle payment failures and retries
    # 4. Store payment transaction details
    
    # For demo purposes, we'll simulate a successful payment
    payment_id = f"pay_{int(datetime.now().timestamp())}_{str(uuid.uuid4())[:8]}"
    
    return {
        "success": True,
        "payment": {
            "id": payment_id,
            "amount": payment_data["amount"],
            "method": payment_data["payment_method"],
            "status": "completed",
            "processed_at": datetime.utcnow().isoformat()
        }
    }
