from dataclasses import dataclass
from datetime import datetime


@dataclass
class Offering:
    id: int | None
    company_id: int
    description: str
    is_open: bool
    created_date: datetime

    @staticmethod
    def from_row(row: tuple) -> "Offering":
        return Offering(
            id=row[0],
            company_id=row[1],
            description=row[2],
            is_open=bool(row[3]),
            created_date=datetime.fromisoformat(row[4]),
        )
