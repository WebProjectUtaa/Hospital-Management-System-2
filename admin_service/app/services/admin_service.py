from app.db.models import AdminModel
from app.db.init_db import get_db_connection

class AdminService:
    @staticmethod
    async def list_all_users(conn, role=None):
        """
        Tüm kullanıcıları listele (isteğe bağlı olarak role göre filtreleme).
        """
        return await AdminModel.get_all_users(conn, role)

    @staticmethod
    async def add_user(conn, user_data):
        """
        Yeni bir kullanıcı ekle.
        """
        return await AdminModel.add_user(conn, user_data)

    @staticmethod
    async def update_user(conn, user_id, update_data):
        """
        Kullanıcı bilgilerini güncelle.
        """
        return await AdminModel.update_user(conn, user_id, update_data)

    @staticmethod
    async def delete_user(conn, user_id):
        """
        Kullanıcıyı sil.
        """
        return await AdminModel.delete_user(conn, user_id)

    @staticmethod
    async def list_departments(conn):
        """
        Tüm departmanları listele.
        """
        return await AdminModel.get_departments(conn)

    @staticmethod
    async def add_department(conn, department_name):
        """
        Yeni bir departman ekle.
        """
        return await AdminModel.add_department(conn, department_name)

    @staticmethod
    async def update_department(conn, department_id, update_data):
        """
        Departman bilgilerini güncelle.
        """
        return await AdminModel.update_department(conn, department_id, update_data)

    @staticmethod
    async def delete_department(conn, department_id):
        """
        Departmanı sil.
        """
        return await AdminModel.delete_department(conn, department_id)

    @staticmethod
    async def assign_doctor_to_department(conn, doctor_id, department_id):
        """
        Doktoru belirli bir departmana ata.
        """
        return await AdminModel.assign_doctor_to_department(conn, doctor_id, department_id)

    @staticmethod
    async def list_appointments(conn):
        """
        Tüm randevuları listele.
        """
        return await AdminModel.get_all_appointments(conn)

    @staticmethod
    async def update_appointment(conn, appointment_id, update_data):
        """
        Randevu bilgilerini güncelle.
        """
        return await AdminModel.update_appointment(conn, appointment_id, update_data)

    @staticmethod
    async def delete_appointment(conn, appointment_id):
        """
        Randevuyu sil.
        """
        return await AdminModel.delete_appointment(conn, appointment_id)

    @staticmethod
    async def list_lab_tests(conn):
        """
        Tüm laboratuvar testlerini listele.
        """
        return await AdminModel.get_all_lab_tests(conn)
