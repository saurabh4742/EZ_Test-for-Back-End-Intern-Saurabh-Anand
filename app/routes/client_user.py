from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.utils.security import get_current_user, RoleEnum
from app.services.file_service import generate_download_link, list_uploaded_files, secure_download
from app.database import SessionLocal

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.get("/files")
async def list_files(db: AsyncSession = Depends(get_db), user=Depends(get_current_user)):
    return await list_uploaded_files(user, db)

@router.get("/download-file/{file_id}")
async def generate(file_id: str, db: AsyncSession = Depends(get_db), user=Depends(get_current_user)):
    return await generate_download_link(file_id, user, db)

@router.get("/download/{token}")
async def download(token: str, db: AsyncSession = Depends(get_db), user=Depends(get_current_user)):
    return await secure_download(token, user, db)
