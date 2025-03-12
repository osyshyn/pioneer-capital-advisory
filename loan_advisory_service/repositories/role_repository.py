from sqlalchemy import select
from sqlalchemy.orm import joinedload, selectinload
from loan_advisory_service.db.models.users.role import Role
from loan_advisory_service.repositories.base_repository import BaseRepository
from loan_advisory_service.db.models.users.role import Role


class RoleRepository(BaseRepository):
    async def get_by_id(self, role_id: int) -> Role | None:
        return await self.session.get(Role, role_id)

    async def get_by_name(self, name: str) -> Role | None:
        stmt = select(Role).where(Role.name == name)
        return await self.session.scalar(stmt)

    async def get_all(self) -> list[Role]:
        stmt = select(Role)
        return (await self.session.scalars(stmt)).all()

    async def get_role_with_permission(self, role_id: int):
        stmt = (
            select(Role)
            .options(selectinload(Role.permissions))
            .where(Role.id == role_id)
        )
        result = await self.session.execute(stmt)
        return result.scalars().first()

