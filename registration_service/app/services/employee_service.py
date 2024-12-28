import bcrypt
from app.db.models import Employee, Doctor, Nurse
from app.db.init_db import get_db_connection

class EmployeeService:
    @staticmethod
    async def add_employee(conn, name, surname, role, email, gender, contacts=None, department=None, degree=None, specialization=None, password=None):
        """
        Add a new employee to the database and handle role-specific table entries.
        """
        # Hash the password if provided
        hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8') if password else None

        async with conn.cursor() as cur:
            # Insert into employees table
            await cur.execute("""
                INSERT INTO employees (Employee_name, surname, role, email, gender, contacts, department, Employee_password)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
            """, (name, surname, role, email, gender, contacts, department, hashed_password))
            await conn.commit()

            # Fetch the last inserted employee ID
            await cur.execute("SELECT LAST_INSERT_ID()")
            employee_id = (await cur.fetchone())[0]

            # Role-specific handling
            if role == "doctor":
                if not (degree and specialization):
                    raise ValueError("Doctor must have a degree and specialization.")
                await cur.execute("""
                    INSERT INTO doctors (employee_id, degree, specialization)
                    VALUES (%s, %s, %s)
                """, (employee_id, degree, specialization))
            elif role == "nurse":
                if not degree:
                    raise ValueError("Nurse must have a degree.")
                await cur.execute("""
                    INSERT INTO nurses (employee_id, degree)
                    VALUES (%s, %s)
                """, (employee_id, degree))
            elif role not in ["admin", "receptionist"]:
                raise ValueError(f"Invalid role: {role}")

            await conn.commit()

        return {
            "message": f"{role.capitalize()} {name} {surname} added successfully!",
            "id": employee_id
        }

    @staticmethod
    async def update_employee(conn, employee_id, updates):
        """
        Update an employee's details in the database.
        """
        if "password" in updates:
            updates["password"] = bcrypt.hashpw(updates["password"].encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
        update_fields = ", ".join([f"{key} = %s" for key in updates.keys()])
        query = f"""
        UPDATE employees
        SET {update_fields}
        WHERE id = %s
        """
        async with conn.cursor() as cur:
            await cur.execute(query, (*updates.values(), employee_id))
            await conn.commit()
        return {"message": f"Employee with ID {employee_id} updated successfully!"}

    @staticmethod
    async def get_all_employees(conn):
        """
        Retrieve all employees from the database.
        """
        query = "SELECT * FROM employees"
        async with conn.cursor() as cur:
            await cur.execute(query)
            employees = await cur.fetchall()
        return employees

    @staticmethod
    async def get_employee_by_id(conn, employee_id):
        """
        Retrieve a specific employee by ID from the database.
        """
        query = "SELECT * FROM employees WHERE id = %s"
        async with conn.cursor() as cur:
            await cur.execute(query, (employee_id,))
            employee = await cur.fetchone()
        if not employee:
            raise ValueError(f"Employee with ID {employee_id} not found.")
        return employee

    @staticmethod
    async def delete_employee(conn, employee_id):
        """
        Delete an employee from the database.
        """
        query = "DELETE FROM employees WHERE id = %s"
        async with conn.cursor() as cur:
            await cur.execute(query, (employee_id,))
            await conn.commit()
        return {"message": f"Employee with ID {employee_id} deleted successfully!"}