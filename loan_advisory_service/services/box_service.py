from fastapi import UploadFile, HTTPException
from boxsdk import Client as BoxClient
from boxsdk.exception import BoxAPIException
from loan_advisory_service.db.models.users.user import User
from loan_advisory_service.repositories.user_repository import UserRepository
from loan_advisory_service.schemas.box import BoxFolder, BoxFileResponse


class BoxService:
    def __init__(self, box_client: BoxClient, user_repo: UserRepository):
        self.box_client = box_client
        self.user_repo = user_repo

    async def upload_file(self, folder_id: int, file: UploadFile):
        try:
            folder = self.box_client.folder(folder_id).get()
            uploaded_file = folder.upload_stream(file.file, file.filename)
            shared_link = uploaded_file.get_shared_link(access='open')
            return BoxFileResponse(
                file_id=uploaded_file.id,
                file_name=uploaded_file.name,
                file_url=shared_link
            )
        except BoxAPIException as e:
            raise HTTPException(status_code=400, detail=f'{e}')

    async def create_user_folder(self, user_email: str) -> BoxFolder | None:
        try:
            folder = self.box_client.folder('313199322492').create_subfolder(user_email)
            return BoxFolder(folder_id=folder.id)
        except BoxAPIException as e:
            if e.status == 409:
                raise HTTPException(status_code=400, detail='user with this email already exists')

    async def added_collaboration(self, client_email: str, folder_id: str = None) -> str:
        try:
            folder = self.box_client.folder('313199322492').get()
            folder_id = folder.id
            folder.collaborate_with_login(client_email, 'editor')
            return folder_id
        except BoxAPIException as e:
            if e.status == 409:
                existing_folder = next(
                    f for f in self.box_client.folder('0').get_items() if f.name == 'All_Client_Files')
                existing_folder.collaborate_with_login(client_email, 'editor')
                return existing_folder.id
            return None

    async def clean_all_contents(self) -> dict:
        try:
            root_folder = self.box_client.folder('0')
            items = root_folder.get_items()
            deleted_items_count = 0
            for item in items:
                try:
                    if item.type == 'folder':
                        item.delete()
                    elif item.type == 'file':
                        item.delete()
                    deleted_items_count += 1
                except BoxAPIException as e:
                    print(f"Error deleting item {item.id}: {e}")
                    continue

            return {
                "status": "success",
                "message": f"Deleted {deleted_items_count} items from Box",
                "deleted_count": deleted_items_count
            }

        except BoxAPIException as e:
            raise HTTPException(status_code=400, detail=f"Error cleaning Box contents: {e}")

    async def ensure_user_folder(self, user: User) -> int:
        if user.folder_id is None:
            folder = await self.create_user_folder(user.email)
            user.folder_id = folder.folder_id
            self.user_repo.session.add(user)
            await self.user_repo.session.commit()
        return user.folder_id
