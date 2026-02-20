from datetime import datetime

from pydantic import BaseModel


class CreateOfferingRequest(BaseModel):
    description: str


class UpdateOfferingRequest(BaseModel):
    description: str | None = None
    is_open: bool | None = None


class OfferingResponse(BaseModel):
    id: int
    company_id: int
    description: str
    is_open: bool
    created_date: datetime
