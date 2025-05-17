from passlib.context import CryptContext
from email.message import EmailMessage
import aiosmtplib

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash_password(password: str) -> str:
    return pwd_context.hash(password)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)

SMTP_HOST = "smtp.gmail.com"     # или smtp.gmail.com
SMTP_PORT = 587
SMTP_USER = "grogertm@gmail.com"
SMTP_PASSWORD = "iqhe dcbd mdap qohz"

async def send_verification_email(to_email: str, token: str):
    url = f"http://localhost:8000/verify-email?token={token}"
    message = EmailMessage()
    message["From"] = SMTP_USER
    message["To"] = to_email
    message["Subject"] = "Подтверждение почты"
    message.set_content(f"Здравствуйте! Перейдите по ссылке для подтверждения: {url}")

    await aiosmtplib.send(
        message,
        hostname=SMTP_HOST,
        port=SMTP_PORT,
        username=SMTP_USER,
        password=SMTP_PASSWORD,
        start_tls=True,
    )
