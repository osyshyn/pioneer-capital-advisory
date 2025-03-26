from sqlalchemy import select
from sqlalchemy.orm import joinedload, selectinload
from loan_advisory_service.schemas.notification import CreateNotification
from loan_advisory_service.repositories.base_repository import BaseRepository
from loan_advisory_service.db.models.notifications import Notification, NotificationUser


class NotificationRepository(BaseRepository):

    async def create_notification(self, data: CreateNotification) -> Notification:
        notification = Notification(message=data.message)
        self.session.add(notification)
        await self.session.commit()
        return notification

    async def assign_notification_to_users(self, message_id: int, user_ids: list[int]) -> None:
        user_messages = [NotificationUser(user_id=user_id, notification_id=message_id) for user_id in user_ids]
        self.session.add_all(user_messages)
        await self.session.commit()