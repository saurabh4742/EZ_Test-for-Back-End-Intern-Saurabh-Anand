from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from app.database import SessionLocal
from app.schema.auth import AuthSchema
from app.services.auth_service import signup_user, verify_email, login_user

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/signup")
async def signup(payload: AuthSchema, db: AsyncSession = Depends(get_db)):
   return await signup_user(payload.email, payload.password, payload.role, db)

@router.get("/verify-email/{token}")
async def verify(token: str, db: AsyncSession = Depends(get_db)):
    return await verify_email(token, db)

@router.post("/login")
async def login(payload: AuthSchema, db: AsyncSession = Depends(get_db)):
    return await login_user(payload.email, payload.password, db)