from app.core.config import settings
from app.domain.models import CampusEvent, CampusEventStatus
from app.infrastructure.mail.smtp_email_sender import SMTPEmailSender
from app.infrastructure.pdf.weasyprint_pdf_generator import WeasyPrintPDFGenerator
from app.infrastructure.templates.jinja_renderer import JinjaTemplateRenderer

MONTHS_ES = {
    1: "enero",
    2: "febrero",
    3: "marzo",
    4: "abril",
    5: "mayo",
    6: "junio",
    7: "julio",
    8: "agosto",
    9: "septiembre",
    10: "octubre",
    11: "noviembre",
    12: "diciembre",
}


class ProcessCampusResult:
    def __init__(self) -> None:
        self.renderer = JinjaTemplateRenderer()
        self.pdf_generator = WeasyPrintPDFGenerator(self.renderer)
        self.email_sender = SMTPEmailSender()

    async def execute(self, event: CampusEvent) -> None:
        if event.status == CampusEventStatus.SUCCESS:
            await self._send_welcome_email(event)
            return

        await self._send_internal_error_email(event)

    async def _send_welcome_email(self, event: CampusEvent) -> None:
        enrollment_date = self._format_enrollment_date(event)
        certificate_pdf = self.pdf_generator.generate(
            "certificates/certification.html",
            {
                "user": event.user,
                "convocatoria": event.convocatoria,
                "campus": event.campus,
                "enrollment_date": enrollment_date,
            },
        )

        html = self.renderer.render(
            "emails/welcome.html",
            {
                "user": event.user,
                "convocatoria": event.convocatoria,
                "campus": event.campus,
                "enrollment_date": enrollment_date,
            },
        )

        await self.email_sender.send(
            to_email=event.user.email,
            subject=f"Bienvenido a {event.convocatoria.name}",
            html=html,
            text=f"Bienvenido a {event.convocatoria.name}. Adjuntamos tu certificacion.",
            attachments=[
                (
                    "certificacion.pdf",
                    certificate_pdf,
                    "application/pdf",
                )
            ],
        )

    def _format_enrollment_date(self, event: CampusEvent) -> str:
        if event.enrollment_date is None:
            return "fecha no disponible"

        day = event.enrollment_date.day
        month = MONTHS_ES[event.enrollment_date.month]
        year = event.enrollment_date.year
        return f"{day} de {month} de {year}"

    async def _send_internal_error_email(self, event: CampusEvent) -> None:
        html = self.renderer.render(
            "emails/internal_error.html",
            {
                "event": event,
                "error": event.error,
            },
        )

        await self.email_sender.send(
            to_email=settings.internal_alert_email,
            subject=f"Error en integracion Atnova - Evento {event.event_id}",
            html=html,
            text=event.error.message if event.error else "Error no especificado",
        )
