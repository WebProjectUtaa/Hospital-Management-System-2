import unittest
import sys
import os
import datetime
import jwt
from dotenv import load_dotenv

# Projenin ana dizinini Python path'e ekle
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

from utils.jwt_utils import create_token, verify_token

# .env dosyasındaki SECRET_KEY'i yükle
load_dotenv()
SECRET_KEY = os.getenv("JWT_SECRET_KEY")

class TestJWTUtils(unittest.TestCase):
    def test_create_and_verify_token(self):
        # Örnek kullanıcı ID'si
        user_id = 12345

        # Token oluştur
        token = create_token(user_id, SECRET_KEY)
        self.assertIsNotNone(token, "Token oluşturulamadı")
        
        # Token'ı doğrula
        decoded = verify_token(token, SECRET_KEY)
        self.assertEqual(decoded["user_id"], user_id, "Kullanıcı ID'si eşleşmiyor")
        self.assertIn("exp", decoded, "Expiration tarihi eksik")
        self.assertIn("iat", decoded, "Oluşturulma tarihi eksik")

    def test_invalid_token(self):
        # Geçersiz token kontrolü
        invalid_token = "invalidtoken"
        with self.assertRaises(RuntimeError) as context:
            verify_token(invalid_token, SECRET_KEY)
        self.assertEqual(str(context.exception), "Geçersiz token.")

    def test_expired_token(self):
        # Süresi dolmuş bir token test etmek için yapay bir payload oluşturulur
        expired_payload = {
            "user_id": 12345,
            "exp": datetime.datetime.utcnow() - datetime.timedelta(seconds=1),  # Süresi geçmiş
            "iat": datetime.datetime.utcnow()
        }
        expired_token = jwt.encode(expired_payload, SECRET_KEY, algorithm="HS256")

        with self.assertRaises(RuntimeError) as context:
            verify_token(expired_token, SECRET_KEY)
        self.assertEqual(str(context.exception), "Token süresi dolmuş.")

if __name__ == "__main__":
    unittest.main()
