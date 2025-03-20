from dishka import AsyncContainer, Provider, Scope, make_async_container
from fastapi import Request
from loan_advisory_service.db.setup import (
    get_async_session,
    get_async_sessionmaker,
    get_engine,
)
from redis import Redis
from loan_advisory_service.main.config import (
    DbConfig,
    TokenConfig,
    AppConfig,
    RedisConfig,
    EmailConfig,
    BoxConfig,
    PipeDriveConfig
)
from loan_advisory_service.main.config import load_config
from loan_advisory_service.repositories.perrmision_repository import PermissionRepository
from loan_advisory_service.repositories.user_repository import UserRepository
from loan_advisory_service.repositories.role_repository import RoleRepository
from loan_advisory_service.repositories.survey_repository import SurveyRepository

from loan_advisory_service.services.auth.utils.password import PasswordProcessor
from loan_advisory_service.services.auth.utils.token import JwtTokenProcessor
from loan_advisory_service.services.auth.auth_service import AuthService
from boxsdk import Client as BoxClient
from loan_advisory_service.services.external_clients import (
    get_box_client
)
from loan_advisory_service.services.redis_service import get_redis_client, get_redis_pool
from loan_advisory_service.services.auth.auth_user_provider import AuthUserProvider
from loan_advisory_service.services.email.email_service import EmailService
from loan_advisory_service.services.survey_service import SurveyService
from loan_advisory_service.services.permission_service import PermissionService
from loan_advisory_service.services.role_service import RoleService
from loan_advisory_service.services.user_service import UserService
from loan_advisory_service.services.pipe_drive_service import PipeDriveService

def repository_provider() -> Provider:
    provider = Provider()

    provider.provide(UserRepository, scope=Scope.REQUEST)
    provider.provide(RoleRepository, scope=Scope.REQUEST)
    provider.provide(SurveyRepository, scope=Scope.REQUEST)
    provider.provide(PermissionRepository, scope=Scope.REQUEST)


    return provider


def db_provider() -> Provider:
    provider = Provider()

    provider.provide(get_engine, scope=Scope.APP)
    provider.provide(get_async_sessionmaker, scope=Scope.APP)
    provider.provide(get_async_session, scope=Scope.REQUEST)

    return provider


def service_provider() -> Provider:
    provider = Provider()

    provider.provide(AuthService, scope=Scope.REQUEST)
    provider.provide(AuthUserProvider, scope=Scope.REQUEST)
    provider.provide(EmailService, scope=Scope.REQUEST)
    provider.provide(get_redis_pool, scope=Scope.APP)
    provider.provide(get_redis_client, scope=Scope.REQUEST, provides=Redis)
    provider.provide(PermissionService, scope=Scope.REQUEST)
    provider.provide(SurveyService, scope=Scope.REQUEST)
    provider.provide(RoleService, scope=Scope.REQUEST)
    provider.provide(UserService, scope=Scope.REQUEST)
    provider.provide(PipeDriveService, scope=Scope.REQUEST)
    return provider


def get_db_config() -> DbConfig:
    config = load_config()
    return config.db


def get_token_config() -> TokenConfig:
    config = load_config()
    return config.token


def get_app_config() -> AppConfig:
    config = load_config()
    return config.app


def get_redis_config() -> RedisConfig:
    config = load_config()
    return config.redis


def get_email_config() -> EmailConfig:
    config = load_config()
    return config.email


def get_box_config() -> BoxConfig:
    config = load_config()
    return config.box


def get_pipe_drive_config() -> PipeDriveConfig:
    config = load_config()
    return config.pipe_drive


def config_provider() -> Provider:
    provider = Provider()

    provider.provide(get_db_config, scope=Scope.APP, provides=DbConfig)
    provider.provide(get_token_config, scope=Scope.APP, provides=TokenConfig)
    provider.provide(get_app_config, scope=Scope.APP, provides=AppConfig)
    provider.provide(get_redis_config, scope=Scope.APP, provides=RedisConfig)
    provider.provide(get_email_config, scope=Scope.APP, provides=EmailConfig)
    provider.provide(get_box_config, scope=Scope.APP, provides=BoxConfig)
    provider.provide(get_pipe_drive_config, scope=Scope.APP, provides=PipeDriveConfig)
    return provider


def external_clients_provider() -> Provider:
    provider = Provider()
    provider.provide(get_box_client, scope=Scope.APP, provides=BoxClient)
    return provider


def utils_provider() -> Provider:
    provider = Provider()

    provider.from_context(Request, scope=Scope.REQUEST)
    provider.provide(JwtTokenProcessor, scope=Scope.REQUEST)
    provider.provide(PasswordProcessor, scope=Scope.REQUEST)

    return provider


def setup_providers() -> list[Provider]:
    return [
        config_provider(),
        db_provider(),
        repository_provider(),
        utils_provider(),
        service_provider(),
        external_clients_provider()
    ]


def setup_di() -> AsyncContainer:
    providers = setup_providers()
    return make_async_container(*providers)
