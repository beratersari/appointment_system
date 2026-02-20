from dataclasses import dataclass
from datetime import datetime

from backend.models.enums.appointment_status import AppointmentStatus


@dataclass
class Appointment:
    id: int | None
    company_id: int
    offering_id: int
    customer_name: str
    customer_phone: str
    customer_email: str
    start_date: datetime
    end_date: datetime
    created_date: datetime
    status: AppointmentStatus

    @staticmethod
    def from_row(row: tuple) -> "Appointment":
        return Appointment(
            id=row[0],
            company_id=row[1],
            offering_id=row[2],
            customer_name=row[3],
            customer_phone=row[4],
            customer_email=row[5],
            start_date=datetime.fromisoformat(row[6]),
            end_date=datetime.fromisoformat(row[7]),
            created_date=datetime.fromisoformat(row[8]),
            status=AppointmentStatus(row[9]),
        )
