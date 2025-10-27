# app/services/payment_service.py
import os
import requests

TRIPAY_API_KEY = os.getenv("TRIPAY_API_KEY")
TRIPAY_MERCHANT_CODE = os.getenv("TRIPAY_MERCHANT_CODE")
TRIPAY_PRIVATE_KEY = os.getenv("TRIPAY_PRIVATE_KEY")

BASE_URL = "https://tripay.co.id/api-sandbox"  # pakai sandbox dulu

def create_payment(amount: int, name: str, email: str):
    """
    Buat transaksi pembayaran baru di Tripay
    """
    url = f"{BASE_URL}/transaction/create"
    headers = {"Authorization": f"Bearer {TRIPAY_API_KEY}"}

    payload = {
        "method": "QRIS",  # contoh: qris / bank / ewallet
        "merchant_ref": f"ORDER-{email}",
        "amount": amount,
        "customer_name": name,
        "customer_email": email,
        "order_items": [
            {
                "sku": "CHATBOT-PLAN",
                "name": "Chatbot Premium Plan",
                "price": amount,
                "quantity": 1
            }
        ],
        "return_url": "https://toko-client.com/thanks",
        "expired_time": 24 * 60 * 60,  # 24 jam
        "signature": f"{TRIPAY_MERCHANT_CODE}{email}{amount}{TRIPAY_PRIVATE_KEY}"
    }

    response = requests.post(url, headers=headers, json=payload)
    if response.status_code == 200:
        return response.json()
    return {"error": response.text}