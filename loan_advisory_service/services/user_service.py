from fastapi import HTTPException
from redis import Redis
from sqlalchemy.future import select
from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from loan_advisory_service.repositories.user_repository import UserRepository
from loan_advisory_service.repositories.role_repository import RoleRepository
from loan_advisory_service.services.pipe_drive_service import PipeDriveService


class UserService:
    def __init__(self, redis: Redis, user_repository: UserRepository, role_repository: RoleRepository,
                 pipe_drive_repo: PipeDriveService):
        self.user_repository = user_repository
        self.role_repository = role_repository
        self.pipe_repository = pipe_drive_repo
        self.redis = redis

    async def assign_role(self, user_id: int, role_id: int) -> None:
        user = await self.user_repository.get_users_with_roles(user_id)
        if not user:
            raise HTTPException(status_code=400, detail='User not found')
        role = await self.role_repository.get_by_id(role_id)
        if not role:
            raise HTTPException(status_code=400, detail='Role not found')
        try:
            user.roles.append(role)
            await self.user_repository.session.commit()
            if 'manager' in role.name.lower():
                await self.pipe_repository.create_user(user.email, 'Yura')

        except IntegrityError as e:
            raise HTTPException(status_code=400, detail='Role already assigned')

    async def remove_role(self, user_id: int, role_id: int) -> None:
        user = await self.user_repository.get_users_with_roles(user_id)
        if not user:
            raise HTTPException(status_code=400, detail='User not found')
        role = await self.role_repository.get_by_id(role_id)
        if not role:
            raise HTTPException(status_code=400, detail='Role not found')
        try:
            user.roles.remove(role)
            await self.user_repository.session.commit()
        except SQLAlchemyError as e:
            raise HTTPException(status_code=404, detail="An error occurred while revoking the role")
        except ValueError as e:
            raise HTTPException(status_code=404, detail="the user did not have this role")
