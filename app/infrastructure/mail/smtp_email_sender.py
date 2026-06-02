from email.message import EmailMessage
from email.utils import formataddr
from typing import Iterable

import aiosmtplib
from pydantic import EmailStr

from app.core.config import settings

Attachment = tuple[str, bytes, str]


class SMTPEmailSender:
    async def send(
        self,
        to_email: EmailStr | str,
        subject: str,
        html: str,
        text: str,
        attachments: Iterable[Attachment] | None = None,
    ) -> None:
        message = EmailMessage()
        message["From"] = formataddr((settings.smtp_from_name, settings.smtp_from_email))
        message["To"] = str(to_email)
        message["Subject"] = subject
        message.set_content(text)
        message.add_alternative(html, subtype="html")

        for filename, content, mime_type in attachments or []:
            maintype, subtype = mime_type.split("/", 1)
            message.add_attachment(
                content,
                maintype=maintype,
                subtype=subtype,
                filename=filename,
            )

        smtp_kwargs: dict[str, object] = {
            "hostname": settings.smtp_host,
            "port": settings.smtp_port,
            "start_tls": settings.smtp_start_tls,
        }

        if settings.smtp_username and settings.smtp_password:
            smtp_kwargs["username"] = settings.smtp_username
            smtp_kwargs["password"] = settings.smtp_password

        await aiosmtplib.send(message, **smtp_kwargs)
