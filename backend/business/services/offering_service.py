from datetime import datetime, timezone

from backend.data_access.repositories.offering_repository import OfferingRepository
from backend.models.dtos.offering_dto import (
    CreateOfferingRequest,
    OfferingResponse,
    UpdateOfferingRequest,
)
from backend.models.entities.offering import Offering


class OfferingService:

    def __init__(self) -> None:
        self._repository = OfferingRepository()

    def create_offering(
        self, request: CreateOfferingRequest, company_id: int
    ) -> OfferingResponse:
        offering = Offering(
            id=None,
            company_id=company_id,
            description=request.description,
            is_open=True,
            created_date=datetime.now(timezone.utc),
        )
        created = self._repository.create(offering)
        return self._to_response(created)

    def get_offering(
        self, offering_id: int, company_id: int | None = None
    ) -> OfferingResponse | None:
        offering = self._repository.get_by_id(offering_id)
        if offering is None:
            return None
        if company_id is not None and offering.company_id != company_id:
            return None
        return self._to_response(offering)

    def get_offerings_by_company(
        self, company_id: int
    ) -> list[OfferingResponse]:
        offerings = self._repository.get_by_company_id(company_id)
        return [self._to_response(o) for o in offerings]

    def get_open_offerings_by_company(
        self, company_id: int
    ) -> list[OfferingResponse]:
        offerings = self._repository.get_open_by_company_id(company_id)
        return [self._to_response(o) for o in offerings]

    def update_offering(
        self,
        offering_id: int,
        request: UpdateOfferingRequest,
        company_id: int | None = None,
    ) -> OfferingResponse | None:
        offering = self._repository.get_by_id(offering_id)
        if offering is None:
            return None
        if company_id is not None and offering.company_id != company_id:
            return None

        if request.description is not None:
            offering.description = request.description
        if request.is_open is not None:
            offering.is_open = request.is_open

        updated = self._repository.update(offering)
        return self._to_response(updated)

    @staticmethod
    def _to_response(offering: Offering) -> OfferingResponse:
        return OfferingResponse(
            id=offering.id,
            company_id=offering.company_id,
            description=offering.description,
            is_open=offering.is_open,
            created_date=offering.created_date,
        )
