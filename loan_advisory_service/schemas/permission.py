from pydantic import BaseModel, Field, field_validator, ConfigDict


class UserPermissionResponse(BaseModel):
    name: str
    model_config = ConfigDict(from_attributes=True)


class CreatePermission(BaseModel):
    name: str
    description: str | None


class UpdatePermission(BaseModel):
    description: str


class PermissionResponse(BaseModel):
    id: int
    name: str
    description: str | None

    model_config = ConfigDict(from_attributes=True)
