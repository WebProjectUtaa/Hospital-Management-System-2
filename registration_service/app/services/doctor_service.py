from app.db.models import Doctor, Employee
from app.services.employee_service import EmployeeService

class DoctorService:
    @staticmethod
    async def add_doctor(conn, name, surname, email, gender, contacts, degree, specialization, password):
        # Önce employees tablosuna ekle
        await EmployeeService.add_employee(conn, name, surname, "doctor", email, gender, contacts)
        
        # Son eklenen çalışanın ID'sini al
        employee = await Employee.get_by_email(conn, email)
        if not employee:
            raise ValueError("Employee not found after adding!")

        # doctors tablosuna ekle
        await Doctor.add(conn, employee["id"], degree, specialization, password)
        return {"message": f"Doctor {name} {surname} added successfully!"}

    @staticmethod
    async def get_all_doctors(conn):
        """Tüm doktorları getirir."""
        doctors = await Doctor.get_all(conn)
        return doctors
