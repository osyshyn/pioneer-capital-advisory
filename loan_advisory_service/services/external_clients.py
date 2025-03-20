from boxsdk import JWTAuth, Client as BoxClient
from loan_advisory_service.main.config import BoxConfig


async def get_box_client(box_config: BoxConfig) -> BoxClient:
    auth = JWTAuth.from_settings_file(box_config.file_path)
    return BoxClient(auth)
