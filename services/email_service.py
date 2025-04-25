import smtplib
from email.mime.text import MIMEText
from dotenv import load_dotenv
import os

load_dotenv()

EMAIL_ADDRESS = os.getenv("EMAIL_ADDRESS")
EMAIL_PASSWORD = os.getenv("EMAIL_PASSWORD")

def send_verification_email(email, token):
    verification_url = f"http://localhost:4200/verificar-correo?token={token}"
    msg = MIMEText(f"Por favor, verifica tu cuenta haciendo clic en este enlace: {verification_url}")
    msg["Subject"] = "Verifica tu cuenta"
    msg["From"] = EMAIL_ADDRESS
    msg["To"] = email

    with smtplib.SMTP("smtp.gmail.com", 587) as server:
        server.starttls()
        server.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
        server.send_message(msg)
