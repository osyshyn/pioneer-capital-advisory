from dishka.integrations.fastapi import DishkaRoute, FromDishka
from fastapi import APIRouter, Request, Response, Depends



from loan_advisory_service.schemas.users import (
    TwoFactorLogin,
    UserLogin,
)
from loan_advisory_service.services.auth.auth_service import AuthService


admin_auth_router = APIRouter(prefix="/auth", route_class=DishkaRoute, tags=["ADMIN AUTH"])


@admin_auth_router.post('/2fa/generate-qr')
async def generate_qrcode(data: UserLogin, auth_service: FromDishka[AuthService]):
    result = await auth_service.generate_two_factor_qr_code(data)
    return result


@admin_auth_router.post('/2fa/verify')
async def verify_2fa(data: TwoFactorLogin, auth_service: FromDishka[AuthService]):
    result = await auth_service.validate_two_factor_code(data)
    return result
