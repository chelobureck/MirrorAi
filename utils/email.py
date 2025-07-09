import aiosmtplib
from email.message import EmailMessage
from config.settings import get_settings
import random

settings = get_settings()

async def send_verification_email(to_email: str, token: str, code: str):
    frontend_url = "https://saydeck.onrender.com"  # или адрес вашего фронта
    message = EmailMessage()
    message["From"] = settings.GMAIL_USER
    message["To"] = to_email
    message["Subject"] = "MirrorAi Email Verification"
    message.set_content(
        f"""
Hello!

Thank you for registering with MirrorAi.

Your verification code is:

    {code}

Or simply click the link below to verify your account:
{frontend_url}/api/v1/auth/verify-email?token={token}

If you did not request this, please ignore this email.

Best regards,
RAAIZE squad
"""
    )
    await aiosmtplib.send(
        message,
        hostname="smtp.gmail.com",
        port=587,
        username=settings.GMAIL_USER,
        password=settings.GMAIL_APP_PASSWORD,
        start_tls=True,
    ) 