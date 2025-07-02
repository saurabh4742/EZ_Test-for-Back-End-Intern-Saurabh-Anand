from fastapi import FastAPI
from app.routes import auth, ops_user, client_user
from app.database import create_db
from cryptography.fernet import Fernet
app = FastAPI()


@app.get("/")
def read_root():
    return {"message": "API is running 🚀"}
@app.on_event("startup")
async def startup():
    await create_db()

app.include_router(auth.router, prefix="/auth", tags=["Auth"])
app.include_router(ops_user.router, prefix="/ops", tags=["Ops User"])
app.include_router(client_user.router, prefix="/client", tags=["Client User"])