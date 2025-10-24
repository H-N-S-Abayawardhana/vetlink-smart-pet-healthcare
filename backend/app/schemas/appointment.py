from pydantic import BaseModel, validator
from typing import Optional, List
from datetime import datetime
from app.models.appointment import AppointmentStatus, PaymentStatus
from app.schemas.user import UserResponse

class AppointmentBase(BaseModel):
    veterinarian_id: int
    appointment_date: str
    appointment_time: str
    reason: Optional[str] = None
    
    @validator('appointment_date')
    def validate_date(cls, v):
        try:
            datetime.strptime(v, '%Y-%m-%d')
        except ValueError:
            raise ValueError('Date must be in YYYY-MM-DD format')
        return v
    
    @validator('appointment_time')
    def validate_time(cls, v):
        try:
            datetime.strptime(v, '%H:%M:%S')
        except ValueError:
            raise ValueError('Time must be in HH:MM:SS format')
        return v

class AppointmentCreate(AppointmentBase):
    pass

class AppointmentUpdate(BaseModel):
    appointment_date: Optional[str] = None
    appointment_time: Optional[str] = None
    reason: Optional[str] = None
    status: Optional[AppointmentStatus] = None
    reschedule_reason: Optional[str] = None
    
    @validator('appointment_date')
    def validate_date(cls, v):
        if v is not None:
            try:
                datetime.strptime(v, '%Y-%m-%d')
            except ValueError:
                raise ValueError('Date must be in YYYY-MM-DD format')
        return v
    
    @validator('appointment_time')
    def validate_time(cls, v):
        if v is not None:
            try:
                datetime.strptime(v, '%H:%M:%S')
            except ValueError:
                raise ValueError('Time must be in HH:MM:SS format')
        return v

class AppointmentResponse(AppointmentBase):
    id: int
    user_id: int
    status: AppointmentStatus
    reschedule_reason: Optional[str] = None
    rescheduled_from: Optional[int] = None
    payment_status: PaymentStatus
    created_at: datetime
    updated_at: datetime
    confirmed_at: Optional[datetime] = None
    completed_at: Optional[datetime] = None
    
    # User and veterinarian details
    user_name: Optional[str] = None
    user_email: Optional[str] = None
    user_contact: Optional[str] = None
    veterinarian_name: Optional[str] = None
    veterinarian_email: Optional[str] = None
    veterinarian_contact: Optional[str] = None
    
    class Config:
        from_attributes = True

class AppointmentListResponse(BaseModel):
    appointments: List[AppointmentResponse]
    total: int

class PaymentRequest(BaseModel):
    payment_method: str
    amount: float
    payment_details: Optional[dict] = None

class PaymentResponse(BaseModel):
    id: str
    amount: float
    method: str
    status: str
    processed_at: str

