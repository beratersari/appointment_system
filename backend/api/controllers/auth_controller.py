from fastapi import APIRouter, Depends, HTTPException

from backend.api.dependencies.auth_dependency import (
    CurrentUser,
    RoleRequired,
    get_current_user,
)
from backend.business.services.auth_service import AuthService
from backend.data_access.repositories.user_repository import UserRepository
from backend.models.dtos.auth_dto import (
    LoginRequest,
    RegisterRequest,
    TokenResponse,
    UserResponse,
)
from backend.models.enums.role import Role

router = APIRouter(prefix="/api/auth", tags=["Authentication"])

_service = AuthService()
_user_repository = UserRepository()
_admin_only = RoleRequired(Role.ADMIN)


@router.post("/register", response_model=UserResponse, status_code=201)
def register(
    request: RegisterRequest,
    current_user: CurrentUser = Depends(_admin_only),
) -> UserResponse:
    try:
        return _service.register(request)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/login", response_model=TokenResponse)
def login(request: LoginRequest) -> TokenResponse:
    try:
        return _service.login(request)
    except ValueError as e:
        raise HTTPException(status_code=401, detail=str(e))


@router.get("/me", response_model=UserResponse)
def get_current_user_info(
    current_user: CurrentUser = Depends(get_current_user),
) -> UserResponse:
    user = _user_repository.get_by_id(current_user.id)
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return UserResponse(
        id=user.id,
        username=user.username,
        email=user.email,
        role=user.role,
        company_id=user.company_id,
        created_date=user.created_date,
    )
