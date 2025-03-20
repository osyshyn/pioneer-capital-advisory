from datetime import timedelta
from fastapi import HTTPException

from loan_advisory_service.db.models.users.user import User

from loan_advisory_service.repositories.user_repository import UserRepository
from loan_advisory_service.repositories.role_repository import RoleRepository
from loan_advisory_service.schemas.password import PasswordReset, ChangePasswordRequest
from loan_advisory_service.schemas.tokens import (
    AccessTokenResponse,
    RefreshToken,
    TokensResponse,
    VerificationToken,
)
from loan_advisory_service.schemas.users import UserCreate, UserLogin, TwoFactorResponse, TwoFactorLogin
from loan_advisory_service.services.auth.utils.password import PasswordProcessor
from loan_advisory_service.services.auth.utils.token import JwtTokenProcessor
from loan_advisory_service.main.config import AppConfig
from redis import Redis
from io import BytesIO
import pyotp
import qrcode
import base64


class AuthService:
    def __init__(
            self,
            token_processor: JwtTokenProcessor,
            password_processor: PasswordProcessor,
            user_repository: UserRepository,
            role_repository: RoleRepository,
            app_config: AppConfig,
            redis: Redis,
    ) -> None:
        self.token_processor = token_processor
        self.password_processor = password_processor
        self.user_repository = user_repository
        self.role_repository = role_repository
        self.app_config = app_config
        self.redis = redis

    async def register_user(self, data: UserCreate) -> VerificationToken:
        if await self.user_repository.get_by_email(data.email):
            raise HTTPException(status_code=409, detail="Email already registered")
        user = User(
            phone_number = data.phone_number,
            first_name = data.first_name,
            last_name = data.last_name,
            email=data.email,
            hashed_password=self.password_processor.hash(data.password),
        )
        self.user_repository.add(user)

        role_for_user = await self.role_repository.get_by_name('user')
        await self.user_repository.add_role_to_user(user.id, role_for_user.id)
        await self.user_repository.commit()
        token = self.token_processor.create_verification_token(user.id, [role_for_user.name])

        await self.redis.setex(
            f"email_verification_cooldown:{user.email}",
            timedelta(minutes=1),
            "1",
        )
        return token

    async def authenticate_user(self, data: UserLogin) -> TokensResponse:
        user = await self.user_repository.get_users_with_roles(data.email)

        if not user or not self.password_processor.verify(
                data.password, user.hashed_password
        ):
            raise HTTPException(
                status_code=401,
                detail="Invalid email or password",
            )

        if not user.is_active:
            raise HTTPException(status_code=403, detail="Email not verified")

        return TokensResponse(
            access_token=self.token_processor.create_access_token(
                user.id, [i.name for i in user.roles]
            ),
            refresh_token=self.token_processor.create_refresh_token(
                user.id, [i.name for i in user.roles]
            ),
            token_type="bearer",
        )

    async def refresh_token(self, data: RefreshToken) -> AccessTokenResponse:
        payload = self.token_processor.validate_refresh_token(data.refresh_token)
        return AccessTokenResponse(
            access_token=self.token_processor.create_access_token(
                payload.user_id, payload.user_roles
            ),
            token_type="bearer",
        )

    async def refresh_email_verification(self, email) -> VerificationToken:
        if await self.redis.exists(f"email_verification_cooldown:{email}"):
            raise HTTPException(status_code=400, detail="Wait for cooldown")
        user = await self.user_repository.get_users_with_roles(email)
        if not user:
            raise HTTPException(status_code=400, detail="Email not registered")
        if user.is_active:
            raise HTTPException(status_code=409, detail="Email arleady verified")
        token = self.token_processor.create_verification_token(user.id, [i.name for i in user.roles])
        await self.redis.setex(
            f"email_verification_cooldown:{user.email}",
            timedelta(minutes=1),
            "1",
        )
        return token

    async def activate_user(self, token: str):
        payload = self.token_processor.validate_verification_token(token)
        user = await self.user_repository.get(payload.user_id)
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        if user.is_active:
            return

        user.is_active = True
        await self.user_repository.commit()

        await self.redis.delete(f"email_verification_cooldown:{user.email}")

    async def create_password_verification(
            self, email: str
    ) -> VerificationToken | None:
        user = await self.user_repository.get_by_email(email)
        if not user:
            return

        async with self.redis.pipeline() as pipe:
            old_token, has_cooldown = (
                await pipe.get(f"password_verification_user:{user.id}")
                .exists(f"password_verification_cooldown:{user.id}")
                .execute()
            )
        if old_token:
            if has_cooldown:
                raise HTTPException(status_code=400, detail="Wait for cooldown")
            await self.redis.delete(
                f"password_verification:{old_token}",
                f"password_verification_user:{user.id}",
            )

        token = VerificationToken(
            token=self.token_processor.create_urlsafe_token(),
            expires_in=self.app_config.reset_password_ttl,
        )

        async with self.redis.pipeline() as pipe:
            await pipe.setex(
                f"password_verification:{token.token}",
                timedelta(minutes=self.app_config.reset_password_ttl),
                user.id,
            )
            await pipe.setex(
                f"password_verification_user:{user.id}",
                timedelta(minutes=self.app_config.reset_password_ttl),
                token.token,
            )
            await pipe.setex(
                f"password_verification_cooldown:{user.id}",
                timedelta(minutes=1),
                "1",
            )
            await pipe.execute()

        return token

    async def reset_password(self, data: PasswordReset) -> None:
        user_id = await self.redis.get(f"password_verification:{data.token}")
        if not user_id:
            raise HTTPException(
                status_code=400,
                detail="Token invalid or expired",
            )
        user = await self.user_repository.get(int(user_id))
        user.hashed_password = self.password_processor.hash(data.password)

        await self.user_repository.commit()

        await self.redis.delete(
            f"password_verification:{data.token}",
            f"password_verification_user:{user_id}",
            f"password_verification_cooldown:{user_id}",
        )

    async def generate_two_factor_qr_code(self, data: UserLogin) -> TwoFactorResponse:
        user = await self.user_repository.get_users_with_roles(data.email)
        if not user or not self.password_processor.verify(data.password, user.hashed_password):
            raise HTTPException(status_code=401, detail="Invalid email or password")

        if not user.is_active:
            raise HTTPException(status_code=403, detail="Email not verified")
        if any("admin" in role.name for role in user.roles):
            if user.is_two_factor_enabled == False:
                user.is_two_factor_enabled = True
                secret = pyotp.random_base32()
                user.two_factor_secret = secret

                self.user_repository.add(user)
                await self.user_repository.commit()
            totp = pyotp.TOTP(user.two_factor_secret)
            qr_code_url = totp.provisioning_uri(user.email, issuer_name="MyApp")
            qr_code_image = qrcode.make(qr_code_url)

            buffered = BytesIO()
            qr_code_image.save(buffered, format="PNG")
            qr_code_base64 = base64.b64encode(buffered.getvalue()).decode("utf-8")

            return TwoFactorResponse(qrcode=qr_code_base64)
        raise HTTPException(status_code=403, detail="Access denied")

    async def validate_two_factor_code(self, data: TwoFactorLogin) -> TokensResponse:
        user = await self.user_repository.get_by_email(data.email)

        if not user or not self.password_processor.verify(
                data.password, user.hashed_password
        ):
            raise HTTPException(
                status_code=401,
                detail="Invalid email or password",
            )

        totp = pyotp.TOTP(user.two_factor_secret)
        if totp.verify(data.code,):
            return TokensResponse(
                access_token=self.token_processor.create_access_token(
                    user.id, [i.name for i in user.roles]
                ),
                refresh_token=self.token_processor.create_refresh_token(
                    user.id, [i.name for i in user.roles]
                ),
                token_type="bearer",
            )
        raise HTTPException(status_code=404, detail="Invalid code")
