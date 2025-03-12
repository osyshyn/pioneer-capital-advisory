from dishka.integrations.fastapi import DishkaRoute, FromDishka
from fastapi import APIRouter, Request, Response, Depends
from loan_advisory_service.api.utils.security import bearer
from loan_advisory_service.repositories.perrmision_repository import PermissionRepository
from loan_advisory_service.services.auth.auth_user_provider import AuthUserProvider
from loan_advisory_service.services.permission_service import PermissionService
from loan_advisory_service.schemas.permission import CreatePermission, PermissionResponse, UpdatePermission

admin_permission_router = APIRouter(prefix="/permission", route_class=DishkaRoute, tags=["ADMIN PERMISSION"])


@admin_permission_router.post('', dependencies=[bearer])
async def create_permission(data: list[CreatePermission], permission_service: FromDishka[PermissionService],
                            auth_provide: FromDishka[AuthUserProvider]):
    # await auth_provide.get_current_user(permissions='create_permission')
    await permission_service.create_permission(data)
    return Response(status_code=201)


@admin_permission_router.delete('/{permission_id}', dependencies=[bearer])
async def delete_permission(permission_id: int, permission_service: FromDishka[PermissionService],
                            auth_provide: FromDishka[AuthUserProvider]):
    # await auth_provide.get_current_user(permissions='delete_permission')
    await permission_service.delete_permission(permission_id)
    return Response(status_code=204)


@admin_permission_router.patch('/{permission_id}', dependencies=[bearer])
async def update_permission(permission_id: int, data: UpdatePermission, auth_provide: FromDishka[AuthUserProvider],
                            permission_service: FromDishka[PermissionService]

                            ):
    # await auth_provide.get_current_user(permissions='delete_permission')
    await permission_service.update_permission(permission_id, data)
    return Response(status_code=204)
