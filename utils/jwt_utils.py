import jwt
import datetime

def create_token(payload, secret_key, expires_in=9000):
    """
    Kullanıcı için belirli bir süre geçerli olan JWT token oluşturur.
    """
    now = datetime.datetime.now(datetime.timezone.utc)  # UTC zamanlı datetime
    payload["exp"] = now + datetime.timedelta(seconds=expires_in)
    payload["iat"] = now  # Token oluşturulma zamanı
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
