import os
from dataclasses import dataclass

from dotenv import load_dotenv


@dataclass
class DbConfig:
    host: str
    port: int
    db: str
    user: str
    password: str
    driver: str = "postgresql+asyncpg"

    @staticmethod
    def from_env() -> "DbConfig":
        return DbConfig(
            host=os.getenv("POSTGRES_HOST"),
            port=int(os.getenv("POSTGRES_PORT")),
            db=os.getenv("POSTGRES_DB"),
            user=os.getenv("POSTGRES_USER"),
            password=os.getenv("POSTGRES_PASSWORD"),
        )

    def build_dsn(self) -> str:
        return f"{self.driver}://{self.user}:{self.password}@{self.host}:{self.port}/{self.db}"


@dataclass
class TokenConfig:
    access_secret: bytes
    access_algorithm: str
    access_expire_minutes: int

    refresh_secret: bytes
    refresh_algorithm: str
    refresh_expire_days: int

    verification_secret: bytes
    verification_algorithm: str
    verification_expire_hours: int

    @staticmethod
    def from_env() -> "TokenConfig":
        return TokenConfig(
            access_secret=os.getenv("ACCESS_SECRET").encode(),
            access_algorithm=os.getenv("ACCESS_ALGORITHM"),
            access_expire_minutes=int(os.getenv("ACCESS_EXPIRE_MINUTES")),
            refresh_secret=os.getenv("REFRESH_SECRET").encode(),
            refresh_algorithm=os.getenv("REFRESH_ALGORITHM"),
            refresh_expire_days=int(os.getenv("REFRESH_EXPIRE_DAYS")),
            verification_secret=os.getenv("VERIFICATION_SECRET").encode(),
            verification_algorithm=os.getenv("VERIFICATION_ALGORITHM"),
            verification_expire_hours=int(os.getenv("VERIFICATION_EXPIRE_HOURS")),
        )





@dataclass
class EmailConfig:
    host: str
    port: int
    username: str
    password: str
    templates_dir: str

    @staticmethod
    def from_env() -> "EmailConfig":
        return EmailConfig(
            host=os.getenv("SMTP_HOST"),
            port=int(os.getenv("SMTP_PORT")),
            username=os.getenv("SMTP_USERNAME"),
            password=os.getenv("SMTP_PASSWORD"),
            templates_dir=os.getenv("TEMPLATES_DIR"),
        )


@dataclass
class AppConfig:
    login_url: str
    reset_password_url: str
    reset_password_ttl: int
    success_change_email_url: str
    failed_change_email_url: str

    @staticmethod
    def from_env() -> "AppConfig":
        return AppConfig(
            login_url=os.getenv("FRONTEND_LOGIN_URL"),
            reset_password_url=os.getenv("FRONTEND_RESET_PASSWORD_URL"),
            reset_password_ttl=int(os.getenv("RESET_PASSWORD_TTL_MINUTES")),
            success_change_email_url=os.getenv("SUCCESS_CHANGE_EMAIL_URL"),
            failed_change_email_url=os.getenv("FAILED_CHANGE_EMAIL_URL"),
        )


@dataclass
class RedisConfig:
    host: str
    port: int
    password: str

    @staticmethod
    def from_env() -> "RedisConfig":
        return RedisConfig(
            host=os.getenv("REDIS_HOST"),
            port=int(os.getenv("REDIS_PORT")),
            password=os.getenv("REDIS_PASSWORD"),
        )







@dataclass
class Config:
    db: DbConfig
    token: TokenConfig
    email: EmailConfig
    app: AppConfig
    redis: RedisConfig



def load_config() -> Config:
    load_dotenv()

    return Config(
        db=DbConfig.from_env(),
        token=TokenConfig.from_env(),
        email=EmailConfig.from_env(),
        app=AppConfig.from_env(),
        redis=RedisConfig.from_env(),

    )
