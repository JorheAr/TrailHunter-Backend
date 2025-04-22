from itsdangerous import URLSafeTimedSerializer
import os

SECRET_KEY = os.environ.get("SECRET_KEY", "clave_secreta_segura")
SALT = "email-confirm-salt"

def generate_verification_token(email):
    serializer = URLSafeTimedSerializer(SECRET_KEY)
    return serializer.dumps(email, salt=SALT)

def confirm_verification_token(token, expiration=3600):
    serializer = URLSafeTimedSerializer(SECRET_KEY)
    try:
        email = serializer.loads(token, salt=SALT, max_age=expiration)
    except Exception:
        return None
    return email
