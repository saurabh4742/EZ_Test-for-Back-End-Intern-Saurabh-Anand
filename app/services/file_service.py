import os
import uuid
from fastapi import UploadFile, HTTPException
from app.models.file import File
from app.utils.security import encrypt_token, decrypt_token
from sqlalchemy.future import select

UPLOAD_FOLDER = "./uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

async def upload_file(file: UploadFile, user, db):
    allowed_extensions = {".pptx", ".docx", ".xlsx"}
    filename = file.filename
    ext = os.path.splitext(filename)[1].lower()
    if ext not in allowed_extensions:
        raise HTTPException(status_code=400, detail="Only pptx, docx, and xlsx files are allowed")
    file_id = uuid.uuid4()
    file_path = os.path.join(UPLOAD_FOLDER, str(file_id))
    content = await file.read()
    with open(file_path, "wb") as f:
        f.write(content)
    db_file = File(id=file_id, filename=file.filename, uploader_id=user.id)
    db.add(db_file)
    await db.commit()
    return {"message": "File uploaded successfully"}

async def list_uploaded_files(user, db):
    result = await db.execute(select(File))
    return result.scalars().all()

async def generate_download_link(file_id: str, user, db):
    token = encrypt_token(file_id)
    return {"download_url": f"/client/download/{token}"}

async def secure_download(token: str, user, db):
    if user.role != "client":
        raise HTTPException(status_code=403, detail="Only client users can download files")
    try:
        file_id = decrypt_token(token)
        file = await db.get(File, uuid.UUID(file_id))
        if not file:
            raise HTTPException(status_code=404, detail="File not found")
        file_path = os.path.join(UPLOAD_FOLDER, str(file.id))
        if not os.path.exists(file_path):
            raise HTTPException(status_code=404, detail="File not found on server")
        return {"filename": file.filename, "path": file_path}
    except:
        raise HTTPException(status_code=400, detail="Invalid or expired token")