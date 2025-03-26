from fastapi.datastructures import URL
from dishka.integrations.fastapi import DishkaRoute, FromDishka
from fastapi import APIRouter, Request, Response, Form, File, UploadFile, HTTPException
from loan_advisory_service.api.utils.security import bearer
from loan_advisory_service.main.config import AppConfig
from loan_advisory_service.schemas.request import RequestData
from loan_advisory_service.services.auth.utils.token import JwtTokenProcessor
from loan_advisory_service.repositories.request_repository import RequestRepository
from loan_advisory_service.services.request_service import RequestService
from loan_advisory_service.services.auth.auth_user_provider import AuthUserProvider
request_router = APIRouter(prefix="/request", route_class=DishkaRoute, tags=["REQUEST"])


@request_router.post('/create-request', dependencies=[bearer])
async def create_request(auth_provider: FromDishka[AuthUserProvider],
                         request_service: FromDishka[RequestService],
                         group_text: list[str] = Form(...),
                         question_category: list[str] = Form(...),
                         answer_type: list[str] = Form(...),
                         question_texts: list[str] = Form(...),
                         answer_texts: list[str] = Form(...),
                         files: list[UploadFile] = File(...)):
    data = RequestData(
        group_text=group_text,
        question_category=question_category,
        answer_type=answer_type,
        question_texts=question_texts,
        answer_texts=answer_texts,
        files=files
    )
    user = await auth_provider.get_current_user()
    await request_service.create_request(user, data)
    return Response(status_code=201)


@request_router.post('/refill-the-request/{token}', dependencies=[bearer])
async def refill_the_request(token: str, auth_provider: FromDishka[AuthUserProvider],
                             request_service: FromDishka[RequestService],
                             token_processor: FromDishka[JwtTokenProcessor],
                             group_text: list[str] = Form(...),
                             question_category: list[str] = Form(...),
                             answer_type: list[str] = Form(...),
                             question_texts: list[str] = Form(...),
                             answer_texts: list[str] = Form(...),
                             files: list[UploadFile] = File(...)):
    data = RequestData(
        group_text=group_text,
        question_category=question_category,
        answer_type=answer_type,
        question_texts=question_texts,
        answer_texts=answer_texts,
        files=files
    )
    request_id = token_processor.validate_redirect_token(token)
    user = await auth_provider.get_current_user()
    await request_service.create_request(user, data, request_id)
    return Response(status_code=201)


@request_router.post('/create-shared-link', dependencies=[bearer])
async def create_shared_link(token_processor: FromDishka[JwtTokenProcessor],
                             auth_provider: FromDishka[AuthUserProvider],
                             request_repo: FromDishka[RequestRepository],
                             config: FromDishka[AppConfig]):
    user = await auth_provider.get_current_user()
    user_request = await request_repo.get_existing_request_id(user.id)
    if user_request:
        token = token_processor.create_redirect_token(user_request.request_id)
        link = URL(config.apply_link_url).include_query_params(token=token)
        return Response(str(link))
    raise HTTPException(status_code=400, detail="User hasn't had a request yet")