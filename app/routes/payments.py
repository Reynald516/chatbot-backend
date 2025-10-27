# app/routes/payments.py
from fastapi import APIRouter
from pydantic import BaseModel
from app.services.payment_service import create_payment

router = APIRouter()

class PaymentRequest(BaseModel):
    amount: int
    name: str
    email: str

@router.post("/")
def create_payment_endpoint(request: PaymentRequest):
    result = create_payment(request.amount, request.name, request.email)
    return result