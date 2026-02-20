from dataclasses import dataclass
from datetime import datetime

from backend.models.enums.role import Role


@dataclass
class User:
    id: int | None
    username: str
    password_hash: str
    email: str
    role: Role
    company_id: int | None
    created_date: datetime

    @staticmethod
    def from_row(row: tuple) -> "User":
        return User(
            id=row[0],
            username=row[1],
            password_hash=row[2],
            email=row[3],
            role=Role(row[4]),
            company_id=row[5],
            created_date=datetime.fromisoformat(row[6]),
        )
