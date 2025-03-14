from dishka.integrations.fastapi import DishkaRoute, FromDishka
from fastapi import APIRouter, Request, Response, Depends
from loan_advisory_service.api.utils.security import bearer
from loan_advisory_service.schemas.users import AssignRole
from loan_advisory_service.services.auth.auth_user_provider import AuthUserProvider
from loan_advisory_service.services.user_service import UserService

admin_user = APIRouter(prefix="/user", route_class=DishkaRoute, tags=["ADMIN USER"])


@admin_user.post('/{user_id}/assign-role')
async def assign_role(user_id: int, data: AssignRole, auth_provider: FromDishka[AuthUserProvider],
                      user_service: FromDishka[UserService]):
    # await auth_provider.get_current_user(permissions='manage_users_and_roles')
    await user_service.assign_role(role_id=data.role_id, user_id=user_id)
    return Response(status_code=204)

@admin_user.delete('/{user_id}/remove-role')
async def assign_role(user_id: int, data: AssignRole, auth_provider: FromDishka[AuthUserProvider],
                      user_service: FromDishka[UserService]):
    # await auth_provider.get_current_user(permissions='manage_users_and_roles')
    await user_service.remove_role(role_id=data.role_id, user_id=user_id)
    return Response(status_code=204)

