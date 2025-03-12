from fastapi import HTTPException
from loan_advisory_service.schemas.role import UpdateRole, CreateRole
from loan_advisory_service.db.models.users.role import Role
from loan_advisory_service.db.models.users.permission import Permission
from loan_advisory_service.repositories.role_repository import RoleRepository
from loan_advisory_service.repositories.perrmision_repository import PermissionRepository
from redis import Redis
from sqlalchemy.future import select
from sqlalchemy.exc import IntegrityError, SQLAlchemyError


class RoleService:
    def __init__(self, redis: Redis, role_repository: RoleRepository, permission_repository: PermissionRepository):
        self.role_repository = role_repository
        self.permission_repository = permission_repository
        self.redis = redis

    async def create_role(self, data: CreateRole) -> None:
        try:
            stmt = select(Permission).filter(Permission.id.in_(data.permissions))
            permissions = await self.role_repository.session.execute(stmt)
            result = permissions.scalars().all()
            new_role = Role(
                name=data.name,
                description=data.description,
                permissions=result
            )

            self.role_repository.session.add(new_role)
            await self.role_repository.session.commit()
            await self.redis.sadd(new_role.name, *[i.name for i in result])
        except IntegrityError as e:
            await self.role_repository.session.rollback()
            error_message = str(e.orig)
            raise HTTPException(status_code=400, detail=f"A role '{error_message}' already exists")

    async def update_role(
            self,
            role_id: int,
            data: UpdateRole,
    ):
        try:
            async with self.role_repository.session.begin():

                role = await self.role_repository.get_role_with_permission(role_id)
                if not role:
                    raise HTTPException(status_code=400, detail="Role not found")
                old_name = role.name
                role.name = data.name
                role.description = data.description
                self.role_repository.session.add(role)
                permissions_to_add = None
                if data.permission_to_add:
                    permissions_to_add = await self.permission_repository.get_permissions_by_ids(data.permission_to_add)
                    role.permissions.extend(permissions_to_add)
                permissions_to_remove = None
                if data.permission_to_delete:
                    permissions_to_remove = await self.permission_repository.get_permissions_by_ids(
                        data.permission_to_delete)
                    for perm in permissions_to_remove:
                        if perm in role.permissions:
                            role.permissions.remove(perm)

                self.role_repository.session.add(role)
                await self.role_repository.session.commit()
            if old_name != data.name:
                await self.redis.delete(old_name)
                await self.redis.sadd(role.name, *[perm.name for perm in role.permissions])
            elif old_name == data.name and permissions_to_add:
                await self.redis.sadd(role.name, *[perm.name for perm in permissions_to_add])
            if data.permission_to_delete:
                await self.redis.srem(role.name, *[perm.name for perm in permissions_to_remove])



        except SQLAlchemyError as e:
            await self.role_repository.session.rollback()
            raise HTTPException(status_code=500, detail=f"Database error occurred {e}") from e
        except Exception as e:
            await self.role_repository.session.rollback()
            raise HTTPException(status_code=500, detail=f"An unexpected error occurred {e}") from e

    async def delete_role(self, role_id: int):
        role = await self.role_repository.get_role_with_permission(role_id)
        if not role:
            raise HTTPException(status=400,detail="Role not found")
        await self.redis.srem(role.name, *[perm.name for perm in role.permissions])
        await self.role_repository.session.delete(role)
        await self.role_repository.session.commit()
