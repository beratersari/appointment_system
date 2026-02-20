from datetime import datetime

from pydantic import BaseModel, EmailStr

from backend.models.enums.appointment_status import AppointmentStatus


class CreateAppointmentRequest(BaseModel):
    company_id: int
    offering_id: int
    customer_name: str
    customer_phone: str
    customer_email: EmailStr
    start_date: datetime
    end_date: datetime


class UpdateAppointmentRequest(BaseModel):
    offering_id: int | None = None
    customer_name: str | None = None
    customer_phone: str | None = None
    customer_email: EmailStr | None = None
    start_date: datetime | None = None
    end_date: datetime | None = None
    status: AppointmentStatus | None = None


class AppointmentResponse(BaseModel):
    id: int
    company_id: int
    offering_id: int
    customer_name: str
    customer_phone: str
    customer_email: str
    start_date: datetime
    end_date: datetime
    created_date: datetime
    status: AppointmentStatus
