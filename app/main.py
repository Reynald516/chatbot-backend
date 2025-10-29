# app/main.py
from dotenv import load_dotenv
load_dotenv()  # biar .env kebaca
from fastapi import FastAPI
from app.routes import auth, clients, chat, payments
from app.database import Base, engine
from app.routes import webhook
app.include_router(webhook.router)

# Buat tabel di DB kalau belum ada
Base.metadata.create_all(bind=engine)

app = FastAPI(title="Chatbot AI Business Backend")

# Include routess
app.include_router(auth.router, prefix="/auth", tags=["auth"])
app.include_router(clients.router, prefix="/clients", tags=["clients"])
app.include_router(chat.router, prefix="/chat", tags=["chat"])
app.include_router(payments.router, prefix="/payments", tags=["payments"])

@app.get("/")
def root():
    return {"message": "Backend chatbot siap jual!"}