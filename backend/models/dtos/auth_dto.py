from datetime import datetime

from pydantic import BaseModel, EmailStr

from backend.models.enums.role import Role


class RegisterRequest(BaseModel):
    username: str
    password: str
    email: EmailStr
    role: Role
    company_id: int | None = None


class LoginRequest(BaseModel):
    username: str
    password: str


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"


class UserResponse(BaseModel):
    id: int
    username: str
    email: str
    role: Role
    company_id: int | None
    created_date: datetime
