from pydantic import BaseModel, Field, field_validator, ConfigDict


class BoxFolder(BaseModel):
    folder_id: int


class BoxFileResponse(BaseModel):
    file_id: int
    file_name: str
    file_url: str
