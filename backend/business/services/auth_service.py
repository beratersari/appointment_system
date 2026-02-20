from datetime import datetime, timedelta, timezone

import bcrypt
import jwt

from backend.data_access.repositories.user_repository import UserRepository
from backend.models.dtos.auth_dto import (
    LoginRequest,
    RegisterRequest,
    TokenResponse,
    UserResponse,
)
from backend.models.entities.user import User
from backend.models.enums.role import Role

SECRET_KEY = "appointment-system-secret-key-change-in-production"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60

DEFAULT_ADMIN_USERNAME = "admin"
DEFAULT_ADMIN_PASSWORD = "admin123"
DEFAULT_ADMIN_EMAIL = "admin@appointment-system.com"


class AuthService:

    def __init__(self) -> None:
        self._repository = UserRepository()

    def seed_default_admin(self) -> None:
        existing = self._repository.get_by_username(DEFAULT_ADMIN_USERNAME)
        if existing is not None:
            return

        password_hash = bcrypt.hashpw(
            DEFAULT_ADMIN_PASSWORD.encode("utf-8"), bcrypt.gensalt()
        ).decode("utf-8")

        admin = User(
            id=None,
            username=DEFAULT_ADMIN_USERNAME,
            password_hash=password_hash,
            email=DEFAULT_ADMIN_EMAIL,
            role=Role.ADMIN,
            company_id=None,
            created_date=datetime.now(timezone.utc),
        )
        self._repository.create(admin)

    def register(self, request: RegisterRequest) -> UserResponse:
        existing = self._repository.get_by_username(request.username)
        if existing is not None:
            raise ValueError("Username already exists")

        existing_email = self._repository.get_by_email(request.email)
        if existing_email is not None:
            raise ValueError("Email already exists")

        if request.role == Role.COMPANY and request.company_id is None:
            raise ValueError("company_id is required for company role")

        password_hash = bcrypt.hashpw(
            request.password.encode("utf-8"), bcrypt.gensalt()
        ).decode("utf-8")

        user = User(
            id=None,
            username=request.username,
            password_hash=password_hash,
            email=request.email,
            role=request.role,
            company_id=request.company_id,
            created_date=datetime.now(timezone.utc),
        )

        created = self._repository.create(user)
        return self._to_response(created)

    def login(self, request: LoginRequest) -> TokenResponse:
        user = self._repository.get_by_username(request.username)
        if user is None:
            raise ValueError("Invalid username or password")

        if not bcrypt.checkpw(
            request.password.encode("utf-8"),
            user.password_hash.encode("utf-8"),
        ):
            raise ValueError("Invalid username or password")

        token = self._create_access_token(user)
        return TokenResponse(access_token=token)

    @staticmethod
    def _create_access_token(user: User) -> str:
        expire = datetime.now(timezone.utc) + timedelta(
            minutes=ACCESS_TOKEN_EXPIRE_MINUTES
        )
        payload = {
            "sub": str(user.id),
            "username": user.username,
            "role": user.role.value,
            "company_id": user.company_id,
            "exp": expire,
        }
        return jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)

    @staticmethod
    def decode_token(token: str) -> dict:
        return jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])

    @staticmethod
    def _to_response(user: User) -> UserResponse:
        return UserResponse(
            id=user.id,
            username=user.username,
            email=user.email,
            role=user.role,
            company_id=user.company_id,
            created_date=user.created_date,
        )
