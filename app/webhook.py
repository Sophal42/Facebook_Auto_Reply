from app.agent import reply
from app.config import settings
from app.messenger import send_message
from fastapi import APIRouter, HTTPException, Query, Request, Response

router = APIRouter()


@router.get("/webhook")
async def verify_webhook(
    mode: str = Query(..., alias="hub.mode"),
    token: str = Query(..., alias="hub.verify_token"),
    challenge: str = Query(..., alias="hub.challenge"),
):
    if mode == "subscribe" and token == settings.fb_verify_token:
        return Response(content=challenge, media_type="text/plain")
    raise HTTPException(status_code=403, detail="Verification failed")


@router.post("/webhook")
async def receive_message(request: Request):
    data = await request.json()
    if data.get("object") == "page":
        for entry in data.get("entry", []):
            for messaging_event in entry.get("messaging", []):
                if "message" in messaging_event and not messaging_event[
                    "message"
                ].get("is_echo"):
                    sender_id = messaging_event["sender"]["id"]
                    message_text = messaging_event["message"].get("text")
                    if message_text:
                        reply_text = await reply(sender_id, message_text)
                        await send_message(sender_id, reply_text)
    return "EVENT_RECEIVED"