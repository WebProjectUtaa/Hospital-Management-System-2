from app.db.models import Employee, Doctor, Nurse
from app.utils.security import hash_password

class EmployeeService:
    @staticmethod
    async def add_employee(
        conn, name, surname, role, email, gender, contacts=None, department=None, degree=None, specialization=None, password=None
    ):
        hashed_password = hash_password(password) if password else None
        await Employee.add(conn, name, surname, email, gender, contacts, department)

        async with conn.cursor() as cur:
            await cur.execute("SELECT LAST_INSERT_ID()")
            employee_id = (await cur.fetchone())[0]

        if role == "doctor":
            if not (degree and specialization):
                raise ValueError("Doctor must have a degree and specialization.")
            await Doctor.add(conn, employee_id, degree, specialization, hashed_password)
        
        elif role == "nurse":
            if not degree:
                raise ValueError("Nurse must have a degree.")
            await Nurse.add(conn, employee_id, degree, hashed_password)
        
        elif role not in ["admin", "receptionist"]:
            raise ValueError(f"Invalid role: {role}")

        return {
            "message": f"{role.capitalize()} {name} {surname} added successfully!",
            "id": employee_id
        }

    @staticmethod
    async def update_employee(
        conn, employee_id, name=None, surname=None, role=None, contacts=None, department=None, password=None
    ):
        if password:
            password = hash_password(password)
        await Employee.update(conn, employee_id, name, surname, role, contacts, department, password)
        return {"message": f"Employee with ID {employee_id} updated successfully!"}



    @staticmethod
    async def delete_employee(conn, employee_id):
        await Employee.delete(conn, employee_id)
        return {"message": f"Employee with ID {employee_id} deleted successfully!"}

    @staticmethod
    async def get_all_employees(conn):
        employees = await Employee.get_all(conn)
        return employees

    @staticmethod
    async def update_employee(
        conn, employee_id, name=None, surname=None, role=None, contacts=None, department=None, password=None
    ):
        if password:
            password = hash_password(password)
        await Employee.update(conn, employee_id, name, surname, role, contacts, department, password)
        return {"message": f"Employee with ID {employee_id} updated successfully!"}