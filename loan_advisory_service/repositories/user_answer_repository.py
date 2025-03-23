from sqlalchemy import select
from sqlalchemy.orm import joinedload, selectinload
# from loan_advisory_service.schemas.request import AnswerCreateSchema
from loan_advisory_service.repositories.base_repository import BaseRepository
from loan_advisory_service.db.models.user_answer import Answer


class UserAnswersRepository(BaseRepository):
    async def get_by_id(self, answer_id: int) -> Answer | None:
        return await self.session.get(Answer, answer_id)

    async def get_by_request(self, request_id: int) -> list[Answer]:
        stmt = select(Answer).where(Answer.request_id == request_id)
        return (await self.session.scalars(stmt)).all()

    # async def create_many_answers(self, request_id: int, answers_data: list[AnswerCreateSchema]):
    #     """Додає список відповідей до БД за один коміт, прив'язуючи їх до request_id"""
    #     answers = [Answer(request_id=request_id, **data.model_dump()) for data in answers_data]
    #     self.session.add_all(answers)  # Додаємо всі об'єкти одним запитом
    #     await self.session.commit()  # Виконуємо один коміт
    #     return answers