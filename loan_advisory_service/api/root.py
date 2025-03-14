from loan_advisory_service.api.admin.admin_root import admin_api_router
from loan_advisory_service.api.auth import auth_router
from loan_advisory_service.api.survey import survey_router
from loan_advisory_service.api.user import user_router
from fastapi import APIRouter

api_router = APIRouter(prefix="/api")

api_router.include_router(admin_api_router)
api_router.include_router(auth_router)
api_router.include_router(survey_router)
api_router.include_router(user_router)
