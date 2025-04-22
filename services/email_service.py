import smtplib
from email.mime.text import MIMEText

def send_verification_email(email, token):
    verification_url = f"http://localhost:4200/verificar-correo?token={token}"
    msg = MIMEText(f"Por favor, verifica tu cuenta haciendo clic en este enlace: {verification_url}")
    msg["Subject"] = "Verifica tu cuenta"
    msg["From"] = "trailhuntersupp@gmail.com"
    msg["To"] = email

    with smtplib.SMTP("smtp.gmail.com", 587) as server:
        server.starttls()
        server.login("trailhuntersupp@gmail.com", "blof jbix onwa wzwd")
        server.send_message(msg)
