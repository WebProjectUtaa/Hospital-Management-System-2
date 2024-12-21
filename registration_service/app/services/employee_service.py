from app.db.models import Employee

class EmployeeService:
    @staticmethod
    async def add_employee(conn, name, surname, role, email, gender, contacts=None, department=None, current_user_role="admin"):
        if current_user_role != "admin":
            raise ValueError("Unauthorized: Only admins can add employees.")

        await Employee.add(conn, name, surname, role, email, gender, contacts, department)
        return {"message": f"Employee {name} {surname} added successfully!"}

    @staticmethod
    async def get_all_employees(conn):
        employees = await Employee.get_all(conn)
        return employees

    @staticmethod
    async def update_employee(conn, employee_id, name=None, surname=None, contacts=None):
        if not (name or surname or contacts):
            raise ValueError("At least one field (name, surname, contacts) must be provided to update.")

        await Employee.update(conn, employee_id, name, surname, contacts)
        return {"message": f"Employee with ID {employee_id} updated successfully!"}

    @staticmethod
    async def delete_employee(conn, employee_id):
        await Employee.delete(conn, employee_id)
        return {"message": f"Employee with ID {employee_id} deleted successfully!"}
