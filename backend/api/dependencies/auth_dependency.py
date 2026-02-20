from dataclasses import dataclass

from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

from backend.business.services.auth_service import AuthService
from backend.models.enums.role import Role

_bearer_scheme = HTTPBearer()
_auth_service = AuthService()


@dataclass
class CurrentUser:
    id: int
    username: str
    role: Role
    company_id: int | None


def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(_bearer_scheme),
) -> CurrentUser:
    try:
        payload = _auth_service.decode_token(credentials.credentials)
        return CurrentUser(
            id=int(payload["sub"]),
            username=payload["username"],
            role=Role(payload["role"]),
            company_id=payload.get("company_id"),
        )
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired token",
        )


class RoleRequired:
    def __init__(self, *allowed_roles: Role) -> None:
        self._allowed_roles = allowed_roles

    def __call__(
        self, current_user: CurrentUser = Depends(get_current_user)
    ) -> CurrentUser:
        if current_user.role not in self._allowed_roles:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="You do not have permission to perform this action",
            )
        return current_user
