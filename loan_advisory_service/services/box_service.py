from fastapi import UploadFile
from boxsdk import Client as BoxClient


class BoxService:
    def __init__(self, box_client: BoxClient):
        self.box_client = box_client

    async def upload_file(self, file: UploadFile):
        folder = self.box_client.folder("0")
        uploaded_file = folder.upload_stream(file.file, file.filename)
        file_id = uploaded_file.id

        file_url = self.box_client.file(file_id).get_shared_link()

        return {
            "file_id": file_id,
            "file_name": uploaded_file.name,
            "file_url": file_url,
            "message": "File uploaded successfully"
        }
