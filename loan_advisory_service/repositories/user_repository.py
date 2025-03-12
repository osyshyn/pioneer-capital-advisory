from sqlalchemy import select
from sqlalchemy.orm import joinedload, selectinload

from loan_advisory_service.db.models.users.user import User
from loan_advisory_service.repositories.base_repository import BaseRepository
from loan_advisory_service.db.models.users.role import Role
from loan_advisory_service.db.models.users.user_role import UserRole

class UserRepository(BaseRepository):
    async def get(self, user_id: int) -> User | None:
        return await self.session.get(User, user_id)

    async def get_password(self, user_id: int) -> str:
        stmt = select(User.hashed_password).where(User.id == user_id)
        return (await self.session.execute(stmt)).scalar_one()

    async def get_by_email(self, email: str) -> User | None:
        stmt = (
            select(User)
            .where(User.email == email)
        )
        return await self.session.scalar(stmt)

    async def add_role_to_user(self, user_id: int, role_id: int)->None:
        user_role = UserRole(user_id=user_id, role_id=role_id)

        self.session.add(user_role)
        await self.session.commit()

    async def get_users_with_roles(self, user_id_or_email: int | str) -> User | None:
        filter_field = User.id if isinstance(user_id_or_email, int) else User.email
        filter_value = user_id_or_email

        stmt = (
            select(User)
            .where(filter_field == filter_value)
            .options(selectinload(User.roles))
        )

        return await self.session.scalar(stmt)

