from pydantic import BaseModel, EmailStr
from enum import Enum

class RoleEnum(str, Enum):
    ops = "ops"
    client = "client"

class AuthSchema(BaseModel):
    email: EmailStr
    password: str
    role: RoleEnum  # <-- Add this
