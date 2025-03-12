from pydantic import BaseModel,ConfigDict
from typing import List, Optional
from enum import Enum


class QuestionType(str, Enum):
    text = "text"
    number = "number"
    choice = "choice"


class AnswerOptionSchemaCreate(BaseModel):
    text: str


    model_config = ConfigDict(from_attributes=True)

class QuestionSchemaCreate(BaseModel):
    text: str
    type: QuestionType
    order: int
    options: Optional[List[AnswerOptionSchemaCreate]] = None


    model_config = ConfigDict(from_attributes=True)

class QuestionGroupSchemaCreate(BaseModel):
    title: str
    order: int
    questions: List[QuestionSchemaCreate]

    model_config = ConfigDict(from_attributes=True)


class AnswerOptionSchemaResponse(BaseModel):
    id:int
    text: str

    model_config = ConfigDict(from_attributes=True)


class QuestionSchemaResponse(BaseModel):
    id: int
    text: str
    type: QuestionType
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
    text: str


class QuestionUpdateSchema(BaseModel):
    id: Optional[int] = None
    text: Optional[str] = None
    type: Optional[QuestionType] = None
    order: Optional[int] = None
    options: Optional[List[AnswerOptionUpdateSchema]] = None


class QuestionGroupUpdateSchema(BaseModel):
    title: Optional[str] = None
    order: Optional[int] = None
    questions: Optional[List[QuestionUpdateSchema]] = None
