import jwt
import datetime

def create_token(user_id, secret_key):
    """
    Kullanıcı için JWT token oluşturur.
    """
    payload = {
        "user_id": user_id,
        "exp": datetime.datetime.utcnow() + datetime.timedelta(days=1),  # 1 gün geçerli
        "iat": datetime.datetime.utcnow()  # Token oluşturulma zamanı
    }
    token = jwt.encode(payload, secret_key, algorithm="HS256")
    return token

def verify_token(token, secret_key):
    """
    JWT token doğrular ve payload'ı döner.
    """
    try:
        decoded_payload = jwt.decode(token, secret_key, algorithms=["HS256"])
        return decoded_payload  # Doğruysa payload döner
    except jwt.ExpiredSignatureError:
        raise RuntimeError("Token süresi dolmuş.")
    except jwt.InvalidTokenError:
        raise RuntimeError("Geçersiz token.")
