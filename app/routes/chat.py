# app/routes/chat.py
from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy.orm import Session
from app.services.chatbot_engine import ask_gpt
from app.services.trial import check_trial_status
from app.database import get_db
from app.models import Client, Chat

router = APIRouter()

class ChatRequest(BaseModel):
    client_id: int
    message: str

@router.post("/")
def chat_endpoint(request: ChatRequest, db: Session = Depends(get_db)):
    # Cek status trial
    is_active, message = check_trial_status(db, request.client_id)
    if not is_active:
        return {"response": message}
    # Pastikan client ada & aktif
    client = db.query(Client).filter(Client.id == request.client_id).first()
    if not client:
        raise HTTPException(404, detail="Client tidak ditemukan")
    if not client.active:
        raise HTTPException(403, detail="Client tidak aktif")

    # Panggil LLM
    reply = ask_gpt(request.message)

    # Simpan ke DB
    db.add(Chat(client_id=client.id, user_message=request.message, bot_message=reply))
    db.commit()

    return {"response": reply}

# (Opsional) Lihat chat log client
@router.get("/{client_id}/logs")
def get_chat_logs(client_id: int, db: Session = Depends(get_db)):
    chats = (
        db.query(Chat)
        .filter(Chat.client_id == client_id)
        .order_by(Chat.timestamp.desc())
        .limit(50)
        .all()
    )
    return [
        {
            "id": c.id,
            "timestamp": c.timestamp,
            "user_message": c.user_message,
            "bot_message": c.bot_message,
        }
        for c in chats
    ]