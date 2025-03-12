from dishka.integrations.fastapi import DishkaRoute, FromDishka
from fastapi import APIRouter, Request, Response, Depends
from loan_advisory_service.api.utils.security import bearer
from loan_advisory_service.schemas.role import CreateRole, UpdateRole
from loan_advisory_service.services.auth.auth_user_provider import AuthUserProvider
from loan_advisory_service.services.role_service import RoleService

admin_role_router = APIRouter(prefix="/role", route_class=DishkaRoute, tags=["ADMIN ROLE"])


@admin_role_router.post('', dependencies=[bearer])
async def create_role(date: CreateRole, auth_provider: FromDishka[AuthUserProvider],
                      role_service: FromDishka[RoleService]):
    # await auth_provider.get_current_user(permissions='manage_users_and_role')
    await role_service.create_role(date)
    return Response(status_code=201)


@admin_role_router.patch('/{role_id}', dependencies=[bearer])
async def update_role(role_id: int, data: UpdateRole, auth_provider: FromDishka[AuthUserProvider],
                      role_service: FromDishka[RoleService]):
    # await auth_provider.get_current_user(permissions='manage_users_and_roles')
    await role_service.update_role(role_id, data)

    return Response(status_code=204)


@admin_role_router.delete('/{role_id}', dependencies=[bearer])
async def delete_role(role_id: int, auth_provider: FromDishka[AuthUserProvider],
                      role_service: FromDishka[RoleService]):
    # await auth_provider.get_current_user(permissions='manage_users_and_roles')
    await role_service.delete_role(role_id)
    return Response(status_code=204)
