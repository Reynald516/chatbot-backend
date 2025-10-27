# app/services/chatbot_engine.py
import os
import requests
import time

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

def ask_gpt(prompt: str):
    """
    Kirim pesan ke OpenAI API dan ambil respon.
    Kalau gagal konek (misal sinyal / blokir), balas fallback.
    """
    if not OPENAI_API_KEY:
        return "OPENAI_API_KEY belum diset di .env"

    headers = {
        "Authorization": f"Bearer {OPENAI_API_KEY}",
        "Content-Type": "application/json"
    }

    data = {
        "model": "gpt-4o-mini",
        "messages": [{"role": "user", "content": prompt}],
        "temperature": 0.7
    }

    # Coba 3x untuk jaga koneksi unstable
    for attempt in range(3):
        try:
            r = requests.post(
                "https://api.openai.com/v1/chat/completions",
                json=data,
                headers=headers,
                timeout=30
            )
            # Kalau respon normal
            if r.status_code == 200:
                return r.json()["choices"][0]["message"]["content"]
            # Kalau respon error dari OpenAI
            else:
                return f"⚠ OpenAI Error {r.status_code}: {r.text}"

        except requests.exceptions.ConnectionError:
            print(f"[Retry {attempt+1}] Koneksi gagal, coba lagi...")
            time.sleep(2)

        except requests.exceptions.Timeout:
            print(f"[Retry {attempt+1}] Timeout koneksi, coba lagi...")
            time.sleep(2)

        except Exception as e:
            print(f"❌ Error tidak terduga: {e}")
            return "⚠ Terjadi error saat menghubungi server AI."

    # Kalau 3x percobaan gagal semua
    return "⚠ Maaf, server AI sedang tidak bisa diakses. Coba lagi nanti ya."