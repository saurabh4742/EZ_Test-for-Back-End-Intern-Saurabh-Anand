from fastapi import APIRouter, UploadFile, File, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from app.utils.security import get_current_user, RoleEnum
from app.services.file_service import upload_file
from app.database import SessionLocal

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/upload")
async def upload(file: UploadFile = File(...), db: AsyncSession = Depends(get_db), user=Depends(get_current_user)):
    if user.role != RoleEnum.ops:
        raise HTTPException(status_code=403, detail="Only ops can upload")
    return await upload_file(file, user, db)