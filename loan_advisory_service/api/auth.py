from dishka.integrations.fastapi import DishkaRoute, FromDishka
from fastapi import APIRouter, Request, Response
from fastapi.datastructures import URL
from fastapi.responses import RedirectResponse
from loan_advisory_service.db.models.users.user import User
from loan_advisory_service.api.utils.security import bearer
from loan_advisory_service.main.config import AppConfig
from loan_advisory_service.schemas.password import (
    ChangePasswordRequest,
    PasswordReset,
    PasswordResetRequest,
)
from loan_advisory_service.schemas.tokens import (
    AccessTokenResponse,
    RefreshToken,
    TokensResponse,
)
from loan_advisory_service.schemas.users import (
    UserCreate,
    UserEmail,
    UserLogin,
)
from loan_advisory_service.services.auth.auth_service import AuthService
from loan_advisory_service.services.auth.auth_user_provider import AuthUserProvider
from loan_advisory_service.services.email.email_service import EmailService
from sqlalchemy.orm import selectinload
from sqlalchemy.future import select

auth_router = APIRouter(prefix="/auth", route_class=DishkaRoute, tags=["AUTH"])


@auth_router.post("/register")
async def register_user(
        auth_service: FromDishka[AuthService],
        data: UserCreate,
        email_service: FromDishka[EmailService],
        request: Request,
) -> Response:
    token = await auth_service.register_user(data)
    url = request.url_for("activate_user").include_query_params(token=token.token)

    await email_service.send_verification_email(data.email, str(url), token.expires_in)
    return Response(status_code=204)


@auth_router.post("/resend-verification")
async def resend_verification_email(
        email_service: FromDishka[EmailService],
        auth_service: FromDishka[AuthService],
        request: Request,
        data: UserEmail,
) -> Response:
    token = await auth_service.refresh_email_verification(data.email)
    url = request.url_for("activate_user").include_query_params(token=token.token)

    await email_service.send_verification_email(data.email, str(url), token.expires_in)
    return Response(status_code=204)


@auth_router.get("/verify")
async def activate_user(
        auth_service: FromDishka[AuthService], token: str, config: FromDishka[AppConfig]
) -> RedirectResponse:
    await auth_service.activate_user(token)
    return RedirectResponse(url=config.login_url)


@auth_router.post("/login")
async def login(
        auth_service: FromDishka[AuthService],
        data: UserLogin,
) -> TokensResponse:
    return await auth_service.authenticate_user(data)


@auth_router.post("/refresh")
async def token_refresh(
        auth_service: FromDishka[AuthService],
        data: RefreshToken,
) -> AccessTokenResponse:
    return await auth_service.refresh_token(data)



@auth_router.post("/password/forgot")
async def forgot_password(
        email_service: FromDishka[EmailService],
        auth_service: FromDishka[AuthService],
        data: PasswordResetRequest,
        config: FromDishka[AppConfig],
) -> Response:
    token = await auth_service.create_password_verification(data.email)
    if token:
        url = URL(config.reset_password_url).include_query_params(token=token.token)
        await email_service.send_password_reset_email(
            to_email=data.email, link=str(url), expires_in=token.expires_in
        )

    return Response(status_code=204)


@auth_router.post("/password/reset")
async def reset_password(
        data: PasswordReset,
        auth_service: FromDishka[AuthService],
) -> Response:
    await auth_service.reset_password(data)
    return Response(status_code=204)
