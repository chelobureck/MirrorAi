import aiosmtplib
from email.message import EmailMessage
from config.settings import get_settings

settings = get_settings()

async def send_verification_email(to_email: str, token: str):
    message = EmailMessage()
    message["From"] = settings.GMAIL_USER
    message["To"] = to_email
    message["Subject"] = "Код подтверждения"
    message.set_content(f"Ваш код подтверждения: {token}")

    await aiosmtplib.send(
        message,
        hostname="smtp.gmail.com",
        port=587,
        username=settings.GMAIL_USER,
        password=settings.GMAIL_APP_PASSWORD,
        start_tls=True,
    ) 