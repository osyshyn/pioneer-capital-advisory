from pydantic import BaseModel, ConfigDict
from typing import List, Optional
from loan_advisory_service.db.models.admin.question import QuestionTypeEnum

class AnswerOptionSchemaCreate(BaseModel):
    text: str

    model_config = ConfigDict(from_attributes=True)


class QuestionSchemaCreate(BaseModel):
    text: str
    sub_text: str | None
    is_required: bool
    type: QuestionTypeEnum
    order: int
    options: Optional[List[AnswerOptionSchemaCreate]] = None

    model_config = ConfigDict(from_attributes=True)


class QuestionGroupSchemaCreate(BaseModel):
    title: str
    order: int
    questions: List[QuestionSchemaCreate]

    model_config = ConfigDict(from_attributes=True)


class AnswerOptionSchemaResponse(BaseModel):
    id: int
    text: str

    model_config = ConfigDict(from_attributes=True)


class QuestionSchemaResponse(BaseModel):
    id: int
    text: str
    sub_text: str | None
    is_required: bool
    type: QuestionTypeEnum
    order: int
    options: Optional[List[AnswerOptionSchemaResponse]] = None

    model_config = ConfigDict(from_attributes=True)


class QuestionGroupSchemaResponse(BaseModel):
    id: int
    title: str
    order: int
    questions: List[QuestionSchemaResponse]

    model_config = ConfigDict(from_attributes=True)


class AnswerOptionUpdateSchema(BaseModel):
    id: Optional[int] = None
    text: str =None


class QuestionUpdateSchema(BaseModel):
    id: Optional[int] = None
    text: Optional[str] = None
    sub_text:  Optional[str]=None
    is_required:Optional[bool]= None
    type: Optional[QuestionTypeEnum] = None
    order: Optional[int] = None
    options: Optional[List[AnswerOptionUpdateSchema]] = None


class QuestionGroupUpdateSchema(BaseModel):
    title: Optional[str] = None
    order: Optional[int] = None
    questions: Optional[List[QuestionUpdateSchema]] = None
