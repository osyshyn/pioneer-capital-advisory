from pydantic import BaseModel, Field, field_validator, ConfigDict
from loan_advisory_service.schemas.permission import PermissionResponse


class CreateRole(BaseModel):
    name: str
    description: str | None
    permissions: list[int]


class ResponseRoleWithPermission(BaseModel):
    id: int
    name: str
    description: str | None
    permissions: list[PermissionResponse]


class UpdateRole(BaseModel):
    name: str
    description: str
    permission_to_add: list[int] | None
    permission_to_delete: list[int] | None
