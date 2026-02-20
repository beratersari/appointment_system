from fastapi import APIRouter, Depends, HTTPException

from backend.api.dependencies.auth_dependency import CurrentUser, RoleRequired
from backend.business.services.appointment_service import AppointmentService
from backend.models.dtos.appointment_dto import (
    AppointmentResponse,
    CreateAppointmentRequest,
    UpdateAppointmentRequest,
)
from backend.models.enums.role import Role

router = APIRouter(prefix="/api/appointments", tags=["Appointments"])

_service = AppointmentService()

_admin_only = RoleRequired(Role.ADMIN)
_admin_or_company = RoleRequired(Role.ADMIN, Role.COMPANY)


@router.post("/", response_model=AppointmentResponse, status_code=201)
def create_appointment(
    request: CreateAppointmentRequest,
) -> AppointmentResponse:
    try:
        return _service.create_appointment(request)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/", response_model=list[AppointmentResponse])
def get_all_appointments(
    current_user: CurrentUser = Depends(_admin_or_company),
) -> list[AppointmentResponse]:
    if current_user.role == Role.ADMIN:
        return _service.get_all_appointments()
    return _service.get_all_appointments(company_id=current_user.company_id)


@router.get("/{appointment_id}", response_model=AppointmentResponse)
def get_appointment(
    appointment_id: int,
    current_user: CurrentUser = Depends(_admin_or_company),
) -> AppointmentResponse:
    if current_user.role == Role.ADMIN:
        appointment = _service.get_appointment(appointment_id)
    else:
        appointment = _service.get_appointment(
            appointment_id, company_id=current_user.company_id
        )
    if appointment is None:
        raise HTTPException(status_code=404, detail="Appointment not found")
    return appointment


@router.put("/{appointment_id}", response_model=AppointmentResponse)
def update_appointment(
    appointment_id: int,
    request: UpdateAppointmentRequest,
    current_user: CurrentUser = Depends(_admin_or_company),
) -> AppointmentResponse:
    try:
        if current_user.role == Role.ADMIN:
            appointment = _service.update_appointment(appointment_id, request)
        else:
            appointment = _service.update_appointment(
                appointment_id, request, company_id=current_user.company_id
            )
        if appointment is None:
            raise HTTPException(status_code=404, detail="Appointment not found")
        return appointment
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
