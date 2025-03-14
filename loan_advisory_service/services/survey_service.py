from loan_advisory_service.repositories.survey_repository import SurveyRepository
from loan_advisory_service.schemas.survey import QuestionGroupSchemaCreate, QuestionGroupUpdateSchema, \
    QuestionGroupSchemaResponse


class SurveyService:
    def __init__(self, servey_repository: SurveyRepository):
        self.servey_repository = servey_repository

    async def create_survey(self, data: list[QuestionGroupSchemaCreate]) -> list[QuestionGroupSchemaResponse]:
        created_groups = []
        for group_data in data:
            group = await self.servey_repository.create_question_group(group_data)
            created_groups.append(group)
        return created_groups

    async def update_survey(self, group_id: int, data: QuestionGroupUpdateSchema):
        return await self.servey_repository.update_group(group_id, data)
