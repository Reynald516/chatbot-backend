from fastapi import APIRouter, Depends

router = APIRouter()

@router.post("/login")
async def login_user():
    return {"message": "Login berhasil"}