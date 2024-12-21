from app.db.models import Nurse, Employee
from app.services.employee_service import EmployeeService

class NurseService:
    @staticmethod
    async def add_nurse(conn, name, surname, email, gender, contacts, degree, password):
        # Önce employees tablosuna ekle
        await EmployeeService.add_employee(conn, name, surname, "nurse", email, gender, contacts)
        
        # Son eklenen çalışanın ID'sini al
        employee = await Employee.get_by_email(conn, email)
        if not employee:
            raise ValueError("Employee not found after adding!")

        # nurses tablosuna ekle
        await Nurse.add(conn, employee["id"], degree, password)
        return {"message": f"Nurse {name} {surname} added successfully!"}

    @staticmethod
    async def get_all_nurses(conn):
        nurses = await Nurse.get_all(conn)
        return nurses
