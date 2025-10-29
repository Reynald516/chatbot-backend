# app/routes/webhook.py
from fastapi import APIRouter, Request

router = APIRouter()

@router.get("/webhook")
async def verify_token(request: Request):
    VERIFY_TOKEN = "mysecret123"
    mode = request.query_params.get("hub.mode")
    token = request.query_params.get("hub.verify_token")
    challenge = request.query_params.get("hub.challenge")

    if mode == "subscribe" and token == VERIFY_TOKEN:
        return int(challenge)
    return {"status": "forbidden"}

@router.post("/webhook")
async def receive_message(request: Request):
    body = await request.json()
    print("Incoming message:", body)
    return {"status": "received"}