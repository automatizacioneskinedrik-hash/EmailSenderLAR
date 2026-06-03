from app.core.config import settings
from app.domain.models import CampusEvent, CampusEventStatus
from app.infrastructure.mail.smtp_email_sender import SMTPEmailSender
from app.infrastructure.pdf.weasyprint_pdf_generator import WeasyPrintPDFGenerator
from app.infrastructure.templates.jinja_renderer import JinjaTemplateRenderer


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
        first_name = event.user.name.strip().split()[0]

        certificate_pdf = self.pdf_generator.generate(
            "certificates/certification.html",
            {
                "user": event.user,
                "convocatoria": event.convocatoria,
                "campus": event.campus,
            },
        )

        html = self.renderer.render(
            "emails/welcome.html",
            {
                "user": event.user,
                "first_name": first_name,
                "convocatoria": event.convocatoria,
                "campus": event.campus,
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
