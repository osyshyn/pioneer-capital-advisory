from typing import Optional, List

from pydantic import BaseModel, Field, field_validator, ConfigDict


class CreateNotification(BaseModel):
    message: str

