from sqlalchemy import select
from sqlalchemy.orm import joinedload, selectinload
from loan_advisory_service.repositories.base_repository import BaseRepository
from loan_advisory_service.db.models.request import Request, RequestStatus
from loan_advisory_service.db.models.user_request import UserRequest


class RequestRepository(BaseRepository):
    async def get_by_id(self, request_id: int) -> Request | None:
        return await self.session.get(Request, request_id)

    async def create_request(self, user_id: int, status: str = RequestStatus.pre_loi) -> Request:
        new_request = Request(status=status)
        self.session.add(new_request)
        await self.session.commit()
        user_request = UserRequest(user_id=user_id, request_id=new_request.id)
        self.session.add(user_request)
        await self.session.commit()
        return new_request

    async def add_user_to_request(self, request_id: int, user_id: int)->None:
        user_request = UserRequest(user_id=user_id, request_id=request_id)
        self.session.add(user_request)
        await self.session.commit()

    async def get_existing_request_id(self, user_id: int) -> int | None:
        query = select(UserRequest).where(UserRequest.user_id == user_id)
        result = await self.session.execute(query)
        return result.scalars().first()