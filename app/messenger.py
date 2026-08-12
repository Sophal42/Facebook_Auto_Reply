import logging

from app.config import settings
import httpx

logger = logging.getLogger(__name__)
GRAPH_URL = "https://graph.facebook.com/v19.0/me/messages"


async def send_message(recipient_id: str, text: str):
    payload = {"recipient": {"id": recipient_id}, "message": {"text": text}}
    params = {"access_token": settings.fb_page_access_token}

    async with httpx.AsyncClient() as client:
        try:
            res = await client.post(GRAPH_URL, json=payload, params=params)
            res.raise_for_status()
            logger.info("Sent reply to %s", recipient_id)
        except httpx.HTTPStatusError as error:
            logger.error(
                "Failed to send to %s: %s | Graph API said: %s",
                recipient_id,
                error,
                error.response.text,
            )