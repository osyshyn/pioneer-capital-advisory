from loan_advisory_service.api.utils.security import bearer
from loan_advisory_service.schemas.permission import UserPermissionResponse
from loan_advisory_service.services.auth.auth_user_provider import AuthUserProvider
from loan_advisory_service.repositories.user_repository import UserRepository
from dishka.integrations.fastapi import DishkaRoute, FromDishka
from fastapi import APIRouter, Request, Response

user_router = APIRouter(prefix="/user", route_class=DishkaRoute, tags=["USER"])


@user_router.get('/permissions', dependencies=[bearer])
async def get_permissions(auth_provider: FromDishka[AuthUserProvider],user_repo:FromDishka[UserRepository]):
    user = await auth_provider.get_current_user()
    permission = await user_repo.get_user_permissions(user_id=user.id)

    if not permission.roles:
        return []

    permissions = []
    for role in permission.roles:
        if role.permissions:
            permissions.extend(
                [UserPermissionResponse.model_validate(perm) for perm in role.permissions]
            )

    return permissions