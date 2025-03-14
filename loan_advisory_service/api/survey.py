from loan_advisory_service.schemas.survey import QuestionGroupSchemaResponse
from loan_advisory_service.repositories.survey_repository import SurveyRepository
from loan_advisory_service.services.survey_service import SurveyService
from loan_advisory_service.api.utils.security import bearer
from dishka.integrations.fastapi import DishkaRoute, FromDishka
from fastapi import APIRouter, Request, Response

survey_router = APIRouter(prefix="/survey", route_class=DishkaRoute, tags=["SURVEY"])


@survey_router.get('')
async def get_survey(survey_repository: FromDishka[SurveyRepository]) -> list[QuestionGroupSchemaResponse]:
    groups_survey = await survey_repository.get_survey()
    return [QuestionGroupSchemaResponse.model_validate(schedule) for schedule in groups_survey]

# @survey_router.get('/answer', dependencies=[bearer])
# async def answer_to_survey()