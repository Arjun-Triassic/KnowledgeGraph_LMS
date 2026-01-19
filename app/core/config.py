from functools import lru_cache
from typing import Optional
from dotenv import load_dotenv
from pydantic import AnyUrl, BaseSettings, Field

# ✅ FORCE .env TO LOAD BEFORE ANY SETTINGS ARE READ
load_dotenv()


class Settings(BaseSettings):
    """
    Application configuration loaded from environment variables.
    """

    app_name: str = "KnowledgeGraph LMS"

    database_url: AnyUrl = Field(
        ...,
        env="DATABASE_URL",
        description="Async PostgreSQL URL, e.g. "
        "postgresql+asyncpg://user:password@localhost:5432/knowledgegraph_lms",
    )

    alembic_database_url: Optional[AnyUrl] = Field(
        None,
        env="ALEMBIC_DATABASE_URL",
        description="Sync or async DB URL for Alembic. "
        "Defaults to DATABASE_URL if not set.",
    )

    # Email configuration
    smtp_host: Optional[str] = Field(
        None,
        env="SMTP_HOST",
        description="SMTP server hostname (e.g., smtp.gmail.com)",
    )
    smtp_port: int = Field(
        587,
        env="SMTP_PORT",
        description="SMTP server port (default: 587)",
    )
    smtp_user: Optional[str] = Field(
        None,
        env="SMTP_USER",
        description="SMTP username/email",
    )
    smtp_password: Optional[str] = Field(
        None,
        env="SMTP_PASSWORD",
        description="SMTP password",
    )
    smtp_from_email: Optional[str] = Field(
        None,
        env="SMTP_FROM_EMAIL",
        description="Default sender email address",
    )
    smtp_use_tls: bool = Field(
        True,
        env="SMTP_USE_TLS",
        description="Use TLS for SMTP (default: True)",
    )

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


@lru_cache()
def get_settings() -> Settings:
    """
    Cached settings object.
    """

    return Settings()



