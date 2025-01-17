import bcrypt
from login_service.app.db.models import LoginModel


class LoginService:
    @staticmethod
    async def authenticate_user(conn, email, password, role=None):
        """
        Kullanıcı veya hastayı kimlik doğrulama işlemi.
        """
        # Kullanıcıyı getir
        user = await LoginModel.get_user_by_email(conn, email, role)
        if user and bcrypt.checkpw(password.encode('utf-8'), user['password'].encode('utf-8')):
            return {"id": user['id'], "email": user['email'], "role": user['role']}
        return None

    @staticmethod
    async def authenticate_patient(conn, email, password):
        """
        Hasta kimlik doğrulama işlemi.
        """
        patient = await LoginModel.get_patient_by_email(conn, email)
        if patient and bcrypt.checkpw(password.encode('utf-8'), patient['password'].encode('utf-8')):
            return {"id": patient['patient_id'], "email": patient['email']}
        return None
