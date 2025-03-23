from dishka.integrations.fastapi import DishkaRoute, FromDishka
from fastapi import APIRouter, Request, Response, Form, File, UploadFile
from loan_advisory_service.api.utils.security import bearer
from loan_advisory_service.schemas.request import RequestData
from loan_advisory_service.services.request_service import RequestService
from loan_advisory_service.services.auth.auth_user_provider import AuthUserProvider

request_router = APIRouter(prefix="/request", route_class=DishkaRoute, tags=["REQUEST"])


@request_router.post('/create-request')
async def create_request(auth_provider: FromDishka[AuthUserProvider],
                         request_service: FromDishka[RequestService],
                         answer_type: list[str] = Form(...),
                         question_texts: list[str] = Form(...),
                         answer_texts: list[str] = Form(...),
                         files: list[UploadFile] = File(...)):
    data = RequestData(
        answer_type=answer_type,
        question_texts=question_texts,
        answer_texts=answer_texts,
        files=files
    )
    user = await auth_provider.get_current_user()
    await request_service.create_request(user, data)
    return Response(status_code=201)

# @survey_router.get('/answer', dependencies=[bearer])
# async def answer_to_survey()
