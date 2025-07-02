from sqlalchemy import Column, String, Boolean, Enum
from sqlalchemy.dialects.postgresql import UUID
from app.database import Base
import uuid
import enum

class RoleEnum(str, enum.Enum):
    ops = "ops"
    client = "client"

class User(Base):
    __tablename__ = "users"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    email = Column(String, unique=True, index=True)
    password_hash = Column(String)
    role = Column(Enum(RoleEnum))
    is_verified = Column(Boolean, default=False)