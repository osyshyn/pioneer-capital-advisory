from pydantic import BaseModel, Field, field_validator


class Password(BaseModel):
    password: str = Field(min_length=8, max_length=32)

    @field_validator("password")
    def validate_password(cls, password: str) -> str:
        if not any(c.isupper() for c in password):
            raise ValueError("Password must contain at least one uppercase letter")
        if not any(c.islower() for c in password):
            raise ValueError("Password must contain at least one lowercase letter")
        if not any(c.isdigit() for c in password):
            raise ValueError("Password must contain at least one digit")

        return password


class PasswordResetRequest(BaseModel):
    email: str


class PasswordReset(Password):
    token: str


class ChangePasswordRequest(Password):
    old_password: str
