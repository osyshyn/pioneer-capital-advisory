from fastapi import UploadFile
from boxsdk import Client as BoxClient
from loan_advisory_service.schemas.request import RequestData
from loan_advisory_service.db.models.user_answer import Answer
from loan_advisory_service.db.models.users.user import User
from loan_advisory_service.repositories.user_answer_repository import UserAnswersRepository
from loan_advisory_service.repositories.request_repository import RequestRepository
from loan_advisory_service.services.box_service import BoxService


class RequestService:
    def __init__(self, user_answer_repo: UserAnswersRepository, box_service: BoxService,
                 request_repository: RequestRepository):
        self.box_service = box_service
        self.user_answer_repo = user_answer_repo
        self.request_repository = request_repository

    async def create_request(self, user: User, data: RequestData) -> None:
        parent_folder_id = "0"  # Ідентифікатор батьківської папки
        items = self.box_service.box_client.folder(parent_folder_id).get_items()
        for item in items:
            print(f"Item Name: {item.name}, Item ID: {item.id}")
        # request_id = (await self.request_repository.create_request(user.id)).id
        # user_id = user.id
        # if user.folder_id is None:
        #     folder_id = (await self.box_service.create_user_folder('aaw')).folder_id
        #     user.folder_id = folder_id
        #     self.user_answer_repo.session.add(user)
        #     await self.user_answer_repo.session.commit()
        # else:
        #     folder_id = user.folder_id
        # iter_for_file = 0
        # iter_for_answer_text = 0
        # data_answer = []
        # for index, answer_type in enumerate(data.answer_type):
        #     if answer_type == 'file':
        #         file_data = await self.box_service.upload_file(folder_id, data.files[iter_for_file])
        #         answer = Answer(
        #             user_id = user_id,
        #             request_id=request_id,
        #             question_text=data.question_texts[index],
        #             file_url=file_data.file_url,
        #             file_name=file_data.file_name,
        #             file_id=file_data.file_id
        #         )
        #         data_answer.append(answer)
        #         iter_for_file += 1
        #     elif answer_type == 'text':
        #         answer = Answer(
        #             user_id=user_id,
        #             request_id=request_id,
        #             question_text=data.question_texts[index],
        #             answer_text=data.answer_texts[iter_for_answer_text]
        #         )
        #         data_answer.append(answer)
        #         iter_for_answer_text += 1
        # if data_answer:
        #     self.user_answer_repo.session.add_all(data_answer)
        #     await self.user_answer_repo.session.commit()
