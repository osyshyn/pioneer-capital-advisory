from dishka import AsyncContainer, Provider, Scope, make_async_container
from fastapi import Request
from loan_advisory_service.db.setup import (
    get_async_session,
    get_async_sessionmaker,
    get_engine,
)
from loan_advisory_service.main.config import (
    DbConfig,
    TokenConfig
)
from loan_advisory_service.main.config import load_config



def repository_provider() -> Provider:
    provider = Provider()


    return provider


def db_provider() -> Provider:
    provider = Provider()

    provider.provide(get_engine, scope=Scope.APP)
    provider.provide(get_async_sessionmaker, scope=Scope.APP)
    provider.provide(get_async_session, scope=Scope.REQUEST)

    return provider


def service_provider() -> Provider:
    provider = Provider()

    return provider

def get_db_config() -> DbConfig:
    config = load_config()
    return config.db

def get_token_config() -> TokenConfig:
    config = load_config()
    return config.token



def config_provider() -> Provider:
    provider = Provider()

    provider.provide(get_db_config, scope=Scope.APP, provides=DbConfig)
    provider.provide(get_token_config, scope=Scope.APP, provides=TokenConfig)


    return provider


def utils_provider() -> Provider:
    provider = Provider()

    provider.from_context(Request, scope=Scope.REQUEST)

    return provider


def setup_providers() -> list[Provider]:
    return [
        config_provider(),
        db_provider(),
        repository_provider(),
        utils_provider(),
        service_provider(),
    ]


def setup_di() -> AsyncContainer:
    providers = setup_providers()
    return make_async_container(*providers)
