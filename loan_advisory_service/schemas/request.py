from typing import Optional, List
from fastapi import UploadFile

from pydantic import BaseModel, Field, field_validator, ConfigDict


class RequestData(BaseModel):
    answer_type: List[str]
    question_texts: List[str]
    answer_texts: List[str]
    files: List[UploadFile]
