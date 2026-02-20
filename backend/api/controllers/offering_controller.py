from fastapi import APIRouter, Depends, HTTPException

from backend.api.dependencies.auth_dependency import CurrentUser, RoleRequired
from backend.business.services.offering_service import OfferingService
from backend.models.dtos.offering_dto import (
    CreateOfferingRequest,
    OfferingResponse,
    UpdateOfferingRequest,
)
from backend.models.enums.role import Role

router = APIRouter(prefix="/api/offerings", tags=["Offerings"])

_service = OfferingService()

_admin_or_company = RoleRequired(Role.ADMIN, Role.COMPANY)


@router.post("/", response_model=OfferingResponse, status_code=201)
def create_offering(
    request: CreateOfferingRequest,
    current_user: CurrentUser = Depends(_admin_or_company),
) -> OfferingResponse:
    if current_user.role == Role.COMPANY:
        return _service.create_offering(request, company_id=current_user.company_id)
    raise HTTPException(
        status_code=400,
        detail="Admin cannot create offerings without a company context. Use a company account.",
    )


@router.get("/company/{company_id}", response_model=list[OfferingResponse])
def get_open_offerings_for_company(
    company_id: int,
) -> list[OfferingResponse]:
    return _service.get_open_offerings_by_company(company_id)


@router.get("/", response_model=list[OfferingResponse])
def get_my_offerings(
    current_user: CurrentUser = Depends(_admin_or_company),
) -> list[OfferingResponse]:
    if current_user.role == Role.COMPANY:
        return _service.get_offerings_by_company(current_user.company_id)
    raise HTTPException(
        status_code=400,
        detail="Use GET /api/offerings/company/{company_id} to view a specific company's offerings.",
    )


@router.get("/{offering_id}", response_model=OfferingResponse)
def get_offering(
    offering_id: int,
    current_user: CurrentUser = Depends(_admin_or_company),
) -> OfferingResponse:
    if current_user.role == Role.ADMIN:
        offering = _service.get_offering(offering_id)
    else:
        offering = _service.get_offering(
            offering_id, company_id=current_user.company_id
        )
    if offering is None:
        raise HTTPException(status_code=404, detail="Offering not found")
    return offering


@router.put("/{offering_id}", response_model=OfferingResponse)
def update_offering(
    offering_id: int,
    request: UpdateOfferingRequest,
    current_user: CurrentUser = Depends(_admin_or_company),
) -> OfferingResponse:
    if current_user.role == Role.ADMIN:
        offering = _service.update_offering(offering_id, request)
    else:
        offering = _service.update_offering(
            offering_id, request, company_id=current_user.company_id
        )
    if offering is None:
        raise HTTPException(status_code=404, detail="Offering not found")
    return offering
