import jwt
from cryptography.fernet import Fernet
from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.ext.asyncio import AsyncSession
from app.database import SessionLocal
from app.models.user import User, RoleEnum
from app.config import JWT_SECRET, ENCRYPTION_KEY, EMAIL_SENDER, EMAIL_PASSWORD
from email.message import EmailMessage
import smtplib

fernet = Fernet(ENCRYPTION_KEY.encode())
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")

def create_access_token(data: dict):
    return jwt.encode(data, JWT_SECRET, algorithm="HS256")

def decode_access_token(token: str):
    try:
        return jwt.decode(token, JWT_SECRET, algorithms=["HS256"])
    except jwt.PyJWTError:
        raise HTTPException(status_code=403, detail="Invalid token")

def encrypt_token(data: str) -> str:
    return fernet.encrypt(data.encode()).decode()

def decrypt_token(token: str) -> str:
    return fernet.decrypt(token.encode()).decode()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

async def get_current_user(token: str = Depends(oauth2_scheme), db: AsyncSession = Depends(get_db)):
    payload = decode_access_token(token)
    user = await db.get(User, payload.get("sub"))
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

def get_current_active_user(user=Depends(get_current_user)):
    if not user.is_verified:
        raise HTTPException(status_code=403, detail="Email not verified")
    return user

def require_role(role: RoleEnum):
    def role_checker(user=Depends(get_current_active_user)):
        if user.role != role:
            raise HTTPException(status_code=403, detail="Forbidden")
        return user
    return role_checker

def send_email(to: str, body: str):
    msg = EmailMessage()
    msg["Subject"] = "Verify Your Email"
    msg["From"] = EMAIL_SENDER
    msg["To"] = to
    msg.set_content(body)

    with smtplib.SMTP("smtp.gmail.com", 587) as server:
        server.starttls()
        server.login(EMAIL_SENDER, EMAIL_PASSWORD)
        server.send_message(msg)