from sqlalchemy.ext.asyncio import AsyncSession

from loan_advisory_service.db.models.base import Base


class BaseRepository:
    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    def add(self, model: Base) -> None:
        self.session.add(model)

    async def commit(self) -> None:
        await self.session.commit()

    async def flush(self, models: tuple[Base]) -> None:
        await self.session.flush(models)

    async def refresh(self, model: Base, attrs: tuple[str, ...] | None = None) -> None:
        await self.session.refresh(model, attribute_names=attrs)
