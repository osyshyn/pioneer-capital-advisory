from loan_advisory_service.main.config import PipeDriveConfig
import aiohttp
from aiohttp import ClientSession

class PipeDriveService:
    def __init__(self, pipe_drive_conf: PipeDriveConfig):
        self.api_token = pipe_drive_conf.api_token
        self.base_url = 'https://api.pipedrive.com/v1'

    async def create_user(self,email:str,name:str) -> None:
        url = f"{self.base_url}/users?api_token={self.api_token}"
        data = {
            "name": name,
            "email": email,
            "access": [
                {
                    "app": "sales",
                }
            ],
            "active_flag": True,
        }

        async with ClientSession() as session:
            try:
                async with session.post(url, json=data) as response:
                    response.raise_for_status()
                    result = await response.json()
                    return result
            except aiohttp.ClientResponseError as e:
                pass
            except aiohttp.ClientError as e:
                pass