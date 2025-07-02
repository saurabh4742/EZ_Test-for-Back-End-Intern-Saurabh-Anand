import re
from fastapi import HTTPException

def validate_email(email: str):
    email_regex = r"^[\w\.-]+@[\w\.-]+\.\w+$"
    if not re.match(email_regex, email):
        raise HTTPException(status_code=400, detail="Invalid email format")

def validate_password(password: str):
    if len(password) < 6:
        raise HTTPException(status_code=400, detail="Password must be at least 6 characters long")
