from dishka.integrations.fastapi import DishkaRoute, FromDishka
from fastapi import APIRouter, Request, Response, Depends
from loan_advisory_service.api.utils.security import bearer
from loan_advisory_service.services.auth.auth_user_provider import AuthUserProvider
from loan_advisory_service.schemas.survey import QuestionGroupSchemaCreate, QuestionGroupUpdateSchema
from loan_advisory_service.services.survey_service import SurveyService

admin_survey = APIRouter(prefix="/survey", route_class=DishkaRoute, tags=["ADMIN SURVEY"])


@admin_survey.post('/create-survey', dependencies=[bearer])
async def create_survey(auth_service: FromDishka[AuthUserProvider], survey_services: FromDishka[SurveyService],
                        data: list[QuestionGroupSchemaCreate]):
    result = await survey_services.create_survey(data)
    return result


@admin_survey.put('/{group_id}', dependencies=[bearer])
async def update_group(group_id: int, auth_service: FromDishka[AuthUserProvider],
                       survey_services: FromDishka[SurveyService],
                       data: QuestionGroupUpdateSchema):
    result = await survey_services.update_survey(group_id, data)
    return result
