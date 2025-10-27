# app/models.py
from sqlalchemy import Column, Integer, String, DateTime, Boolean, ForeignKey, Text
from sqlalchemy.orm import relationship
from datetime import datetime
from app.database import Base

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    password_hash = Column(String, nullable=False)
    role = Column(String, default="admin")  # admin / client
    created_at = Column(DateTime, default=datetime.utcnow)

    clients = relationship("Client", back_populates="owner", cascade="all, delete-orphan")

class Client(Base):
    __tablename__ = "clients"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    name = Column(String, nullable=False)
    greeting = Column(String, default="Halo, saya chatbot anda!")
    tone = Column(String, default="friendly")
    trial_start = Column(DateTime, default=datetime.utcnow)
    trial_end = Column(DateTime)
    active = Column(Boolean, default=True)

    owner = relationship("User", back_populates="clients")
    chats = relationship("Chat", back_populates="client", cascade="all, delete-orphan")

class Chat(Base):
    __tablename__ = "chats"
    id = Column(Integer, primary_key=True, index=True)
    client_id = Column(Integer, ForeignKey("clients.id"))
    user_message = Column(Text)
    bot_message = Column(Text)
    timestamp = Column(DateTime, default=datetime.utcnow)

    client = relationship("Client", back_populates="chats")

class Payment(Base):
    __tablename__ = "payments"
    id = Column(Integer, primary_key=True, index=True)
    client_id = Column(Integer, ForeignKey("clients.id"))
    amount = Column(Integer)
    status = Column(String, default="pending")  # pending / paid
    payment_date = Column(DateTime, default=datetime.utcnow)