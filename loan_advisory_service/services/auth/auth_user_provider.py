from fastapi import HTTPException, Request

from loan_advisory_service.db.models.users.user import User
from loan_advisory_service.repositories.user_repository import UserRepository
from loan_advisory_service.services.auth.utils.token import JwtTokenProcessor
from loan_advisory_service.services.permission_service import PermissionService


class AuthUserProvider:
    def __init__(
            self,
            request: Request,
            token_processor: JwtTokenProcessor,
            user_repository: UserRepository,
            permission_service: PermissionService
    ) -> None:
        self.request = request
        self.token_processor = token_processor
        self.user_repository = user_repository
        self.permission_service = permission_service

    def validate(self):
        try:
            token = self.request.headers["Authorization"].lstrip("Bearer").strip()
        except KeyError:
            raise HTTPException(
                status_code=401,
                detail="Not authenticated",
                headers={"WWW-Authenticate": "Bearer"},
            )
        if not token:
            raise HTTPException(
                status_code=401,
                detail="Not authenticated",
                headers={"WWW-Authenticate": "Bearer"},
            )
        return self.token_processor.validate_access_token(token)

    async def get_current_user(
            self, full: bool = False, permissions=None,
    ):
        payload = self.validate()

        if full:
            user = await self.user_repository.get(payload.user_id)
        else:
            user = await self.user_repository.get(payload.user_id)

        if not user:
            raise HTTPException(
                status_code=401,
                detail="Not authenticated",
                headers={"WWW-Authenticate": "Bearer"},
            )
        if not user.is_active:
            raise HTTPException(status_code=403, detail="Email not verified")
        print(await self.permission_service.has_permission(payload.user_roles, permissions))
        print(payload.user_roles)
        if permissions and not await self.permission_service.has_permission(payload.user_roles, permissions):
            raise HTTPException(status_code=403, detail="Permission denied")

        return user
