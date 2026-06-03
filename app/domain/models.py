from enum import StrEnum
from datetime import date

from pydantic import BaseModel, EmailStr, Field


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
    user_created: bool | None = None
    associated: bool | None = None
    response_id: str | None = None


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
