from pydantic import BaseModel, Field, field_validator, ConfigDict

class UserAnswerCreate(BaseModel):
    question_text:str
    answer_text:str