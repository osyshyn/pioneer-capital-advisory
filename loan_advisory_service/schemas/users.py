import json
from enum import Enum

from pydantic import (
    BaseModel,
    ConfigDict,
    EmailStr,
    Field,
    field_validator,
    model_validator,
    validator,
)

from loan_advisory_service.schemas.password import Password


class UserEmail(BaseModel):
    email: EmailStr


class UserCreate(Password):
    first_name: str
    last_name: str
    phone_number: str
    email: EmailStr


class UserLogin(BaseModel):
    email: EmailStr
    password: str


class TwoFactorResponse(BaseModel):
    qrcode: str


class TwoFactorLogin(BaseModel):
    email: EmailStr
    password: str
    code: str


class ChangeEmailRequest(BaseModel):
    new_email: EmailStr
    password: str


class AssignRole(BaseModel):
    role_id: int
