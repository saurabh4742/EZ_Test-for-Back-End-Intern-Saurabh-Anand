import os
from dotenv import load_dotenv
load_dotenv()

JWT_SECRET = os.getenv("JWT_SECRET", "6eae792844db47a7a7275cb57f5a3a8c9b3a2d59d02e4f25b6a6bbf227e51a71")
ENCRYPTION_KEY = "_jQEq1udDCr_77OadXwPP-RZpi8fuPn1oIsNscHczg4="
DATABASE_URL = "postgresql+asyncpg://xxxxxxxxxxxxx/neondb"
EMAIL_SENDER = os.getenv("EMAIL_SENDER", "testing.pvt.ltd12@gmail.com")
EMAIL_PASSWORD = os.getenv("EMAIL_PASSWORD", "XXXXXX")
BASE_URL=os.getenv("BASE_URL","http://localhost:8000")