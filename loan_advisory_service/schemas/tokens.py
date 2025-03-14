from pydantic import BaseModel



class TokenType(BaseModel):
    token_type: str = "bearer"


class AccessToken(BaseModel):
    access_token: str


class RefreshToken(BaseModel):
    refresh_token: str


class AccessTokenResponse(TokenType, AccessToken):
    pass


class TokensResponse(AccessToken, RefreshToken, TokenType):
    pass


class TokenPayload(BaseModel):
    user_id: int
    user_roles: list[str]


class VerificationToken(BaseModel):
    token: str
    expires_in: int
