from sqlalchemy import select, join, delete
from sqlalchemy.orm import selectinload
from loan_advisory_service.repositories.base_repository import BaseRepository
from loan_advisory_service.db.models.users.role import Role
from loan_advisory_service.db.models.users.permission import Permission


class PermissionRepository(BaseRepository):
    async def get_by_id(self, permission_id: int) -> Permission | None:
        return await self.session.get(Permission, permission_id)

    async def get_by_name(self, name: str) -> Permission | None:
        stmt = select(Permission).where(Permission.name == name)
        return await self.session.scalar(stmt)

    async def get_all(self) -> list[Permission]:
        stmt = select(Permission)
        return (await self.session.scalars(stmt)).all()

    async def get_permission_by_role(self, role_id: int):
        stmt = select(Permission).join(Permission.roles).where(Role.id == role_id)
        permissions = await self.session.execute(stmt)
        return permissions.scalars().all()

    async def delete_permission(self, id: int) -> None:
        stmt = delete(Permission).where(Permission.id == id)
        await self.session.execute(stmt)
        await self.session.commit()

    async def get_permissions_by_id_with_role(self, permission_id: int) -> Permission:
        stmt = select(Permission).where(Permission.id == permission_id).options(selectinload(Permission.roles))
        result = await self.session.execute(stmt)
        permissions = result.scalars().first()
        return permissions

    async def get_permissions_by_ids(self, permission_ids: list[int]) -> list[Permission]:
        stmt = select(Permission).filter(Permission.id.in_(permission_ids))
        result = await self.session.execute(stmt)
        permissions = result.scalars().all()
        return permissions
