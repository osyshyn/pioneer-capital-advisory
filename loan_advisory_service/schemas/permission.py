from pydantic import BaseModel, Field, field_validator, ConfigDict


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
