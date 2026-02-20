from datetime import datetime, timezone

from backend.data_access.repositories.appointment_repository import (
    AppointmentRepository,
)
from backend.data_access.repositories.offering_repository import OfferingRepository
from backend.models.dtos.appointment_dto import (
    AppointmentResponse,
    CreateAppointmentRequest,
    UpdateAppointmentRequest,
)
from backend.models.entities.appointment import Appointment
from backend.models.enums.appointment_status import AppointmentStatus


class AppointmentService:

    def __init__(self) -> None:
        self._repository = AppointmentRepository()
        self._offering_repository = OfferingRepository()

    def create_appointment(
        self, request: CreateAppointmentRequest
    ) -> AppointmentResponse:
        if request.end_date <= request.start_date:
            raise ValueError("end_date must be after start_date")

        offering = self._offering_repository.get_by_id(request.offering_id)
        if offering is None:
            raise ValueError("Offering not found")
        if not offering.is_open:
            raise ValueError("Offering is not available")
        if offering.company_id != request.company_id:
            raise ValueError("Offering does not belong to the specified company")

        appointment = Appointment(
            id=None,
            company_id=request.company_id,
            offering_id=request.offering_id,
            customer_name=request.customer_name,
            customer_phone=request.customer_phone,
            customer_email=request.customer_email,
            start_date=request.start_date,
            end_date=request.end_date,
            created_date=datetime.now(timezone.utc),
            status=AppointmentStatus.PENDING,
        )

        created = self._repository.create(appointment)
        return self._to_response(created)

    def get_appointment(
        self, appointment_id: int, company_id: int | None = None
    ) -> AppointmentResponse | None:
        appointment = self._repository.get_by_id(appointment_id)
        if appointment is None:
            return None
        if company_id is not None and appointment.company_id != company_id:
            return None
        return self._to_response(appointment)

    def update_appointment(
        self,
        appointment_id: int,
        request: UpdateAppointmentRequest,
        company_id: int | None = None,
    ) -> AppointmentResponse | None:
        appointment = self._repository.get_by_id(appointment_id)
        if appointment is None:
            return None
        if company_id is not None and appointment.company_id != company_id:
            return None

        if request.offering_id is not None:
            appointment.offering_id = request.offering_id
        if request.customer_name is not None:
            appointment.customer_name = request.customer_name
        if request.customer_phone is not None:
            appointment.customer_phone = request.customer_phone
        if request.customer_email is not None:
            appointment.customer_email = request.customer_email
        if request.start_date is not None:
            appointment.start_date = request.start_date
        if request.end_date is not None:
            appointment.end_date = request.end_date
        if request.status is not None:
            appointment.status = request.status

        if appointment.end_date <= appointment.start_date:
            raise ValueError("end_date must be after start_date")

        updated = self._repository.update(appointment)
        return self._to_response(updated)

    def get_all_appointments(
        self, company_id: int | None = None
    ) -> list[AppointmentResponse]:
        if company_id is not None:
            appointments = self._repository.get_by_company_id(company_id)
        else:
            appointments = self._repository.get_all()
        return [self._to_response(a) for a in appointments]

    @staticmethod
    def _to_response(appointment: Appointment) -> AppointmentResponse:
        return AppointmentResponse(
            id=appointment.id,
            company_id=appointment.company_id,
            offering_id=appointment.offering_id,
            customer_name=appointment.customer_name,
            customer_phone=appointment.customer_phone,
            customer_email=appointment.customer_email,
            start_date=appointment.start_date,
            end_date=appointment.end_date,
            created_date=appointment.created_date,
            status=appointment.status,
        )
