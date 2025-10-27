# app/services/trial.py
from datetime import datetime
from sqlalchemy.orm import Session
from app.models import Client

def check_trial_status(db: Session, client_id: int) -> tuple[bool, str]:
    """
    Cek apakah masa trial client masih aktif.
    Return (True, '') kalau aktif,
    atau (False, pesan error) kalau sudah expired / tidak aktif.
    """
    client = db.query(Client).filter(Client.id == client_id).first()

    if not client:
        return False, "Client tidak ditemukan."

    # kalau status aktif = False
    if not client.active:
        return False, "Akun Anda tidak aktif."

    # kalau tanggal sekarang lewat dari trial_end
    if client.trial_end and datetime.utcnow() > client.trial_end:
        client.active = False
        db.commit()
        return False, "Masa trial Anda telah berakhir. Silakan upgrade untuk melanjutkan layanan."

    return True, ""