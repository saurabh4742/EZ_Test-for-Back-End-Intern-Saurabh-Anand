import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from app.config import EMAIL_SENDER, EMAIL_PASSWORD

async def send_verification_email(to_email: str, verification_link: str):
    subject = "Verify your email address"
    body = f"""
    Hi,

    Please click the link below to verify your email address:

    {verification_link}

    If you did not sign up, please ignore this email.

    Best,
    Your Secure File Sharing App
    """

    msg = MIMEMultipart()
    msg["From"] = EMAIL_SENDER
    msg["To"] = to_email
    msg["Subject"] = subject

    msg.attach(MIMEText(body, "plain"))

    try:
        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
            server.login(EMAIL_SENDER, EMAIL_PASSWORD)
            server.sendmail(EMAIL_SENDER, to_email, msg.as_string())
    except Exception as e:
        print("Email sending failed:", e)
        raise e
