import secrets
from datetime import UTC, datetime, timedelta
from enum import Enum

from fastapi import HTTPException
from jose import jwt
from jose.exceptions import ExpiredSignatureError, JWTError

from loan_advisory_service.main.config import TokenConfig
from loan_advisory_service.schemas.tokens import TokenPayload, VerificationToken


class TokenTypeEnum(str, Enum):
    ACCESS = "access"
    REFRESH = "refresh"
    VERIFICATION = "verification"
    REDIRECT = "redirect"


class JwtTokenProcessor:
    def __init__(self, config: TokenConfig) -> None:
        self.config = config

    def _create_token(
            self,
            sub: int,
            token_type: TokenTypeEnum,
            user_roles: list[str],
            expire_delta: timedelta,
            algorithm: str,
            secret: str,
    ) -> str:
        to_encode = {
            "sub": sub,
            "user_roles": user_roles,
            "token_type": token_type,
            "exp": datetime.now(UTC) + expire_delta,
        }
        return jwt.encode(claims=to_encode, key=secret, algorithm=algorithm)

    def decode_token(
            self,
            token: str,
            token_type: TokenTypeEnum,
            secret: str,
            algorithm: str,
    ) -> TokenPayload:
        try:
            payload = jwt.decode(token=token, key=secret, algorithms=[algorithm])
        except ExpiredSignatureError:
            raise HTTPException(status_code=401, detail="Token has expired")
        except JWTError:
            raise HTTPException(status_code=401, detail="Invalid token")

        if payload.get("token_type") != token_type:
            raise HTTPException(status_code=401, detail="Invalid token type")

        self._validate_expiration(payload)

        try:
            return TokenPayload(
                user_id=int(payload["sub"]),
                user_roles=payload["user_roles"],
            )
        except (ValueError, KeyError):
            raise HTTPException(status_code=401, detail="Invalid token")

    def create_access_token(self, user_id: int, user_roles: list[str]) -> str:
        return self._create_token(
            sub=str(user_id),
            user_roles=user_roles,
            token_type=TokenTypeEnum.ACCESS,
            expire_delta=timedelta(minutes=self.config.access_expire_minutes),
            algorithm=self.config.access_algorithm,
            secret=self.config.access_secret,
        )

    def create_refresh_token(self, user_id: int, user_roles: list[str]) -> str:
        return self._create_token(
            sub=str(user_id),
            user_roles=user_roles,
            token_type=TokenTypeEnum.REFRESH,
            expire_delta=timedelta(days=self.config.refresh_expire_days),
            algorithm=self.config.refresh_algorithm,
            secret=self.config.refresh_secret,
        )

    def validate_access_token(self, token: str) -> TokenPayload:
        return self.decode_token(
            token=token,
            token_type=TokenTypeEnum.ACCESS,
            secret=self.config.access_secret,
            algorithm=self.config.access_algorithm,
        )

    def validate_refresh_token(self, token: str) -> TokenPayload:
        return self.decode_token(
            token=token,
            token_type=TokenTypeEnum.REFRESH,
            secret=self.config.refresh_secret,
            algorithm=self.config.refresh_algorithm,
        )

    def _validate_expiration(self, payload: dict) -> None:
        expiration = payload.get("exp")
        if not expiration or expiration < datetime.now(UTC).timestamp():
            raise HTTPException(status_code=401, detail="Token has expired")

    def create_verification_token(
            self, user_id: int, user_roles: list[str]
    ) -> VerificationToken:
        token = self._create_token(
            sub=str(user_id),
            token_type=TokenTypeEnum.VERIFICATION,
            user_roles=user_roles,
            expire_delta=timedelta(hours=self.config.verification_expire_hours),
            secret=self.config.verification_secret,
            algorithm=self.config.verification_algorithm,
        )
        return VerificationToken(
            token=token, expires_in=self.config.verification_expire_hours
        )

    def validate_verification_token(self, token: str) -> TokenPayload:
        return self.decode_token(
            token=token,
            token_type=TokenTypeEnum.VERIFICATION,
            secret=self.config.verification_secret,
            algorithm=self.config.verification_algorithm,
        )

    def create_redirect_token(self, request_id: int) -> str:
        to_encode = {
            "sub": str(request_id),
            "token_type": TokenTypeEnum.REDIRECT,
            "exp": datetime.now(UTC) + timedelta(days=self.config.refresh_expire_days),
        }
        return jwt.encode(claims=to_encode, key=self.config.redirect_secret, algorithm=self.config.redirect_algorithm)

    def validate_redirect_token(self, token: str) -> int:
        try:
            payload = jwt.decode(token=token, key=self.config.redirect_secret,
                                 algorithms=[self.config.redirect_algorithm])
        except ExpiredSignatureError:
            raise HTTPException(status_code=401, detail="Token has expired")
        except JWTError:
            raise HTTPException(status_code=401, detail="Invalid token")

        if payload.get("token_type") != TokenTypeEnum.REDIRECT:
            raise HTTPException(status_code=401, detail="Invalid token type")

        self._validate_expiration(payload)
        return int(payload['sub'])

    def create_urlsafe_token(self) -> str:
        return secrets.token_urlsafe(32)
