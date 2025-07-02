from fastapi import HTTPException
from passlib.hash import bcrypt
from app.models.user import User
from app.utils.security import create_access_token, encrypt_token, decrypt_token, send_email
from app.config import EMAIL_SENDER
from sqlalchemy.future import select
from app.utils.validator import validate_email, validate_password
from app.services.mail_service import send_verification_email
import uuid
from app.config import BASE_URL

async def signup_user(email: str, password: str, role: str, db):
    existing = await db.execute(select(User).where(User.email == email))
    if existing.scalar():
        raise HTTPException(status_code=400, detail="Email already registered")
    hashed = bcrypt.hash(password)
    new_user = User(email=email, password_hash=hashed, role=role, is_verified=False)
    db.add(new_user)
    await db.commit()
    token = encrypt_token(str(new_user.id))
    verification_url = f"{BASE_URL}/auth/verify-email/{token}"
    await send_verification_email(email, f"Verify your account: {verification_url}")
    return {"message": "Signup successful. Check your email to verify.", "verification_url": verification_url}

async def verify_email(token: str, db):
    try:
        user_id = decrypt_token(token)
        user = await db.get(User, uuid.UUID(user_id))
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        user.is_verified = True
        await db.commit()
        return {"message": "Email verified successfully"}
    except:
        raise HTTPException(status_code=400, detail="Invalid or expired token")

async def login_user(email: str, password: str, db):
    result = await db.execute(select(User).where(User.email == email))
    user = result.scalar()
    if not user or not bcrypt.verify(password, user.password_hash):
        raise HTTPException(status_code=401, detail="Invalid credentials")
    if not user.is_verified:
        raise HTTPException(status_code=403, detail="Email not verified")
    access_token = create_access_token({"sub": str(user.id), "role": user.role})
    return {"access_token": access_token, "token_type": "bearer"}
