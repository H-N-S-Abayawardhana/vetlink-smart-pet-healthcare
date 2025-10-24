from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Enum, Text
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.core.database import Base
import enum

class AppointmentStatus(str, enum.Enum):
    PENDING = "pending"
    ACCEPTED = "accepted"
    REJECTED = "rejected"
    CANCELLED = "cancelled"
    COMPLETED = "completed"

class PaymentStatus(str, enum.Enum):
    UNPAID = "unpaid"
    PAID = "paid"
    REFUNDED = "refunded"

class Appointment(Base):
    __tablename__ = "appointments"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    veterinarian_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    appointment_date = Column(String(10), nullable=False)  # YYYY-MM-DD format
    appointment_time = Column(String(8), nullable=False)   # HH:MM:SS format
    reason = Column(Text, nullable=True)
    status = Column(Enum(AppointmentStatus), default=AppointmentStatus.PENDING, nullable=False)
    reschedule_reason = Column(Text, nullable=True)
    rescheduled_from = Column(Integer, ForeignKey("appointments.id"), nullable=True)
    payment_status = Column(Enum(PaymentStatus), default=PaymentStatus.UNPAID, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
    confirmed_at = Column(DateTime(timezone=True), nullable=True)
    completed_at = Column(DateTime(timezone=True), nullable=True)

    # Relationships
    user = relationship("User", foreign_keys=[user_id], back_populates="user_appointments")
    veterinarian = relationship("User", foreign_keys=[veterinarian_id], back_populates="veterinarian_appointments")
    rescheduled_from_appointment = relationship("Appointment", remote_side=[id])

