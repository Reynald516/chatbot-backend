# seed_client.py
from app.database import SessionLocal, engine
from app.models import Client, User, Base
from datetime import datetime, timedelta

Base.metadata.create_all(bind=engine)
db = SessionLocal()

# bikin user dummy
user = User(email="owner@demo.com", password_hash="dummyhash")
db.add(user)
db.commit()
db.refresh(user)

# bikin client toko
client = Client(
    user_id=user.id,
    name="Toko Demo",
    greeting="Halo! Ada yang bisa dibantu?",
    tone="friendly",
    trial_start=datetime.utcnow(),
    trial_end=datetime.utcnow() + timedelta(days=7),
    active=True
)
db.add(client)
db.commit()
print("SEED DONE. client_id =", client.id)
db.close()