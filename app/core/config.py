from functools import lru_cache

from pydantic import EmailStr, Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")

    app_name: str = "atnova-email-service"
    app_env: str = "local"
    log_level: str = "INFO"

    webhook_secret: str = Field(default="change-me")

    smtp_host: str = "smtp.example.com"
    smtp_port: int = 587
    smtp_username: str = "user@example.com"
    smtp_password: str = "change-me"
    smtp_from_email: EmailStr = "no-reply@example.com"
    smtp_from_name: str = "Atnova Campus"
    smtp_start_tls: bool = True

    internal_alert_email: EmailStr = "gestion@example.com"
    campus_platform_url: str = "https://campus.laruniversity.com/"
    educational_services_contract_url: str = (
        "https://pagoseguro.laruniversity.com/contrato-servicios/"
    )

    gcp_project_id: str | None = None
    gcp_location: str = "us-central1"
    gcp_tasks_queue: str = "email-events"
    gcs_bucket_name: str | None = None


@lru_cache
def get_settings() -> Settings:
    return Settings()


settings = get_settings()
