from fastapi import APIRouter, BackgroundTasks, Depends, status

from app.api.dependencies import validate_webhook_secret
from app.application.use_cases.process_campus_result import ProcessCampusResult
from app.domain.models import CampusEvent, WebhookAcceptedResponse

router = APIRouter(prefix="/webhooks", tags=["webhooks"])


@router.post(
    "/crm-campus-result",
    response_model=WebhookAcceptedResponse,
    status_code=status.HTTP_202_ACCEPTED,
    dependencies=[Depends(validate_webhook_secret)],
)
async def receive_crm_campus_result(
    event: CampusEvent,
    background_tasks: BackgroundTasks,
) -> WebhookAcceptedResponse:
    background_tasks.add_task(ProcessCampusResult().execute, event)
    return WebhookAcceptedResponse(event_id=event.event_id, status="accepted")
