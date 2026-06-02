from fastapi import Header, HTTPException, status

from app.core.config import settings


async def validate_webhook_secret(
    x_secret_token: str | None = Header(default=None, alias="X-Secret-Token"),
) -> None:
    if not x_secret_token or x_secret_token != settings.webhook_secret:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid webhook token",
        )
