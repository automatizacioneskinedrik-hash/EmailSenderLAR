from enum import StrEnum
from datetime import date

from pydantic import AliasChoices, BaseModel, ConfigDict, EmailStr, Field


class CampusEventStatus(StrEnum):
    SUCCESS = "success"
    ERROR = "error"


class UserPayload(BaseModel):
    name: str = Field(min_length=1)
    email: EmailStr
    document: str | None = None


class ConvocatoriaPayload(BaseModel):
    id: str
    name: str


class CampusPayload(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    user_created: bool | None = None
    associated: bool | None = None
    response_id: str | None = None
    username: str | None = Field(
        default=None,
        validation_alias=AliasChoices("username", "user_name", "USERNAME"),
    )
    password: str | None = Field(
        default=None,
        validation_alias=AliasChoices("password", "user_password", "USERPASSWORD"),
    )
    platform_url: str | None = Field(
        default=None,
        validation_alias=AliasChoices("platform_url", "campus_url", "PLATFORM_URL"),
    )
    enrollment_certificate_url: str | None = Field(
        default=None,
        validation_alias=AliasChoices(
            "enrollment_certificate_url",
            "certificate_url",
            "CERTIFICATE_URL",
        ),
    )
    educational_services_contract_url: str | None = Field(
        default=None,
        validation_alias=AliasChoices(
            "educational_services_contract_url",
            "contract_url",
            "CONTRACT_URL",
        ),
    )


class ErrorPayload(BaseModel):
    code: str | None = None
    message: str
    detail: dict | None = None


class CampusEvent(BaseModel):
    event_id: str = Field(min_length=1)
    status: CampusEventStatus
    user: UserPayload
    convocatoria: ConvocatoriaPayload
    enrollment_date: date | None = None
    campus: CampusPayload | None = None
    error: ErrorPayload | None = None


class WebhookAcceptedResponse(BaseModel):
    event_id: str
    status: str


class RenderedEmail(BaseModel):
    subject: str
    html: str
    text: str
