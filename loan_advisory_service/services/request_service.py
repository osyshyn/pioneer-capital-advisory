from fastapi import UploadFile
from boxsdk import Client as BoxClient
from loan_advisory_service.main.config import AppConfig
from loan_advisory_service.schemas.notification import CreateNotification
from loan_advisory_service.schemas.request import RequestData
from loan_advisory_service.db.models.user_answer import Answer
from loan_advisory_service.db.models.users.user import User
from loan_advisory_service.repositories.notifcation_repository import NotificationRepository
from loan_advisory_service.services.auth.utils.token import JwtTokenProcessor
from loan_advisory_service.repositories.user_answer_repository import UserAnswersRepository
from loan_advisory_service.repositories.request_repository import RequestRepository
from loan_advisory_service.services.box_service import BoxService
from loan_advisory_service.services.email.email_service import EmailService
from loan_advisory_service.services.web_socket_service import WebsocketService


class RequestService:
    def __init__(self, user_answer_repo: UserAnswersRepository, box_service: BoxService,
                 request_repository: RequestRepository, token_processor: JwtTokenProcessor,
                 web_socket_service: WebsocketService, notification_repository: NotificationRepository):
        self.box_service = box_service
        self.user_answer_repo = user_answer_repo
        self.request_repository = request_repository
        self.token_processor = token_processor
        self.web_socket_service = web_socket_service
        self.notification_repository = notification_repository

    async def create_request(self, user: User, data: RequestData, request_id: int | None = None) -> None:
        notification = await self.notification_repository.create_notification(
            CreateNotification(message=f'User {user.first_name} create request {request_id}'))
        await self.notification_repository.assign_notification_to_users(notification.id,
                                                                        self.web_socket_service.get_admins())
        await self.web_socket_service.send_admin_message(notification.message)
        # if request_id is None:
        #     request_id = (await self.request_repository.create_request(user.id)).id
        # else:
        #     await self.request_repository.add_user_to_request(request_id, user.id)
        # user_id = user.id
        # folder_id = await self.box_service.ensure_user_folder(user)
        # data_answer = await self._process_answers(data, user_id, request_id, folder_id)
        # if data_answer:
        #     self.user_answer_repo.session.add_all(data_answer)
        #     await self.user_answer_repo.session.commit()
        #     notification = await self.notification_repository.create_notification(
        #         CreateNotification(message=f'User {user.first_name} create request {request_id}'))
        #     await self.notification_repository.assign_notification_to_users(notification.id,
        #                                                                     self.web_socket_service.get_admins())
        #     await self.web_socket_service.send_admin_message(notification.message)

    async def _process_answers(self, data: RequestData, user_id: int, request_id: int, folder_id: str):
        answers = []
        file_index, text_index = 0, 0

        for index, answer_type in enumerate(data.answer_type):
            question_text = data.question_texts[index]

            if answer_type == 'file':
                file = data.files[file_index]
                file_data = await self.box_service.upload_file(folder_id, file)
                answers.append(Answer(
                    group_text=data.group_text[index],
                    question_category=data.question_category[index],
                    user_id=user_id, request_id=request_id, question_text=question_text,
                    file_url=file_data.file_url, file_name=file_data.file_name, file_id=file_data.file_id
                ))
                file_index += 1

            elif answer_type == 'text':
                answers.append(Answer(
                    group_text=data.group_text[index],
                    question_category=data.question_category[index],
                    user_id=user_id, request_id=request_id, question_text=question_text,
                    answer_text=data.answer_texts[text_index]
                ))
                text_index += 1

        return answers
