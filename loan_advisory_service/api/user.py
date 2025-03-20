from loan_advisory_service.api.utils.security import bearer
from loan_advisory_service.schemas.permission import UserPermissionResponse
from loan_advisory_service.services.auth.auth_user_provider import AuthUserProvider
from loan_advisory_service.repositories.user_repository import UserRepository
from dishka.integrations.fastapi import DishkaRoute, FromDishka
from fastapi import APIRouter, Request, Response, UploadFile, File

import requests
user_router = APIRouter(prefix="/user", route_class=DishkaRoute, tags=["USER"])


@user_router.get('/permissions', dependencies=[bearer])
async def get_permissions(auth_provider: FromDishka[AuthUserProvider], user_repo: FromDishka[UserRepository]):
    user = await auth_provider.get_current_user()
    permission = await user_repo.get_user_permissions(user_id=user.id)

    if not permission.roles:
        return []

    permissions = []
    for role in permission.roles:
        if role.permissions:
            permissions.extend(
                [UserPermissionResponse.model_validate(perm) for perm in role.permissions]
            )

    return permissions





# @user_router.get('/upload_file', dependencies=[bearer])
# async def upload_file(box_client: FromDishka[BoxClient], file: UploadFile = File(...)):
#     folder = box_client.folder("0")
#     uploaded_file = folder.upload_stream(file.file, file.filename)
#     file_id = uploaded_file.id
#
#     file_url = box_client.file(file_id).get_shared_link()
#
#     return {
#         "file_id": file_id,
#         "file_name": uploaded_file.name,
#         "file_url": file_url,
#         "message": "File uploaded successfully"
#     }
#
# @user_router.get('/create_user')
# async def create_user():
#     API_TOKEN = "f442e6cac95c0d0e70f07f2f46c9cea1f3053815"
#     BASE_URL = "https://api.pipedrive.com/v1"
#     url = f"{BASE_URL}/users?api_token={API_TOKEN}"
#     data = {
#         "name": 'david',
#         "email": 'urakordiaka6@gmail.com',
#         "active_flag": True,
#         "role_id": 2
#     }
#     response = requests.post(url, json=data)
#     return response.json()