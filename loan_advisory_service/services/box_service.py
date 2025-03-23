from fastapi import UploadFile
from boxsdk import Client as BoxClient
from boxsdk.exception import BoxAPIException
from loan_advisory_service.schemas.box import BoxFolder, BoxFileResponse


class BoxService:
    def __init__(self, box_client: BoxClient):
        self.box_client = box_client

    async def upload_file(self, folder_id: str, file: UploadFile):
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
            print(f"Error uploading file: {e}")
            return None

    async def create_user_folder(self, user_email: str) -> BoxFolder | None:
        try:
            folder = self.box_client.folder('0').create_subfolder('SasdASaqwerweqrDasd112')
            return BoxFolder(folder_id=folder.id)
        except BoxAPIException as e:
            if e.status == 409:
                return None
