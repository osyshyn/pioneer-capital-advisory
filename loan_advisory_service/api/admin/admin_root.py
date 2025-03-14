from loan_advisory_service.api.admin.auth import admin_auth_router
from loan_advisory_service.api.admin.survey import admin_survey
from loan_advisory_service.api.admin.permission import admin_permission_router
from loan_advisory_service.api.admin.role import admin_role_router
from loan_advisory_service.api.admin.user import admin_user
from fastapi import APIRouter

admin_api_router = APIRouter(prefix="/admin")

admin_api_router.include_router(admin_auth_router)
admin_api_router.include_router(admin_survey)
admin_api_router.include_router(admin_permission_router)
admin_api_router.include_router(admin_role_router)
admin_api_router.include_router(admin_user)
