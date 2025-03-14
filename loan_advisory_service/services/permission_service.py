import redis
from fastapi import HTTPException
from typing import List
from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from loan_advisory_service.repositories.perrmision_repository import PermissionRepository
# from loan_advisory_service.services.redis_service import RedisService
from loan_advisory_service.schemas.permission import CreatePermission, PermissionResponse, UpdatePermission
from loan_advisory_service.db.models.users.permission import Permission
from redis import Redis


class PermissionService:
    def __init__(self, redis: Redis, permission_repo: PermissionRepository):
        self.permission_repo = permission_repo
        self.redis = redis

    async def create_permission(self, data: List[CreatePermission]):
        try:
            permissions = [Permission(name=p.name, description=p.description) for p in data]
            self.permission_repo.session.add_all(permissions)
            await self.permission_repo.session.commit()
        except IntegrityError as e:
            await self.permission_repo.session.rollback()
            error_message = str(e.orig)
            for p in data:
                if p.name in error_message:
                    raise HTTPException(status_code=400, detail=f"Permission '{p.name}' already exists")

            raise HTTPException(status_code=400, detail="A permission with this name already exists")

    async def get_permissions_for_roles(self, roles: List[str]) -> dict:
        permissions = {}
        for role in roles:
            role_permissions = await self.redis.smembers(role)
            permissions[role] = role_permissions
        return permissions

    async def has_permission(self, roles: List[str], required_permission: str) -> bool:
        permissions = await self.get_permissions_for_roles(roles)
        for role, perms in permissions.items():
            if required_permission in perms:
                return True
        return False

    async def delete_permission(self, permission_id: int) -> None:
        permissions_with_role = await self.permission_repo.get_permissions_by_id_with_role(permission_id)
        if not permissions_with_role:
            raise HTTPException(status_code=400, detail='Permission not found')
        role_permission = permissions_with_role.roles
        await self.permission_repo.delete_permission(permission_id)
        if role_permission:
            for role in role_permission:
                await self.redis.srem(role.name, permissions_with_role.name)

    async def update_permission(self, permission_id: int, data: UpdatePermission) -> None:
        permission = await self.permission_repo.get_by_id(permission_id)
        if not permission:
            raise HTTPException(status_code=400, detail="Permission not found")
        permission.description = data.description
        self.permission_repo.session.add(permission)
        await self.permission_repo.commit()
