import jwt
import datetime
from dotenv import load_dotenv
import os

load_dotenv()
SECRET_KEY = os.getenv("JWT_SECRET_KEY")

def create_token(payload, secret_key=SECRET_KEY):
    """
    JWT token oluştur.
    """
    payload.update({
        "exp": datetime.datetime.utcnow() + datetime.timedelta(days=1),
        "iat": datetime.datetime.utcnow()
    })
    return jwt.encode(payload, secret_key, algorithm="HS256")

def verify_token(token, secret_key=SECRET_KEY):
    """
    JWT token doğrula.
    """
    try:
        return jwt.decode(token, secret_key, algorithms=["HS256"])
    except jwt.ExpiredSignatureError:
        raise ValueError("Token expired.")
    except jwt.InvalidTokenError:
        raise ValueError("Invalid token.")
