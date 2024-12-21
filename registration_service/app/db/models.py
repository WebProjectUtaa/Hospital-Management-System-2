class Employee:
    @staticmethod
    async def add(conn, name, surname, role, email, gender, contacts=None, department=None):
        async with conn.cursor() as cursor:
            await cursor.execute(
                """
                INSERT INTO employees (Employee_name, surname, role, email, gender, contacts, department)
                VALUES (%s, %s, %s, %s, %s, %s, %s)
                """,
                (name, surname, role, email, gender, contacts, department)
            )
            await conn.commit()

    @staticmethod
    async def get_all(conn):
        async with conn.cursor() as cursor:
            await cursor.execute("SELECT * FROM employees")
            return await cursor.fetchall()

    @staticmethod
    async def get_by_id(conn, employee_id):
        async with conn.cursor() as cursor:
            await cursor.execute("SELECT * FROM employees WHERE id = %s", (employee_id,))
            return await cursor.fetchone()

    @staticmethod
    async def get_by_email(conn, email):
        async with conn.cursor() as cursor:
            await cursor.execute("SELECT * FROM employees WHERE email = %s", (email,))
            return await cursor.fetchone()

    @staticmethod
    async def update(conn, employee_id, name=None, surname=None, contacts=None):
        async with conn.cursor() as cursor:
            await cursor.execute(
                """
                UPDATE employees SET 
                Employee_name = COALESCE(%s, Employee_name), 
                surname = COALESCE(%s, surname),
                contacts = COALESCE(%s, contacts)
                WHERE id = %s
                """,
                (name, surname, contacts, employee_id)
            )
            await conn.commit()

    @staticmethod
    async def delete(conn, employee_id):
        async with conn.cursor() as cursor:
            await cursor.execute("DELETE FROM employees WHERE id = %s", (employee_id,))
            await conn.commit()


class Doctor:
    @staticmethod
    async def add(conn, employee_id, degree, specialization, password):
        async with conn.cursor() as cursor:
            await cursor.execute(
                """
                INSERT INTO doctors (id, degree, specialization, Employee_password)
                VALUES (%s, %s, %s, %s)
                """,
                (employee_id, degree, specialization, password)
            )
            await conn.commit()

    @staticmethod
    async def get_all(conn):
        async with conn.cursor() as cursor:
            await cursor.execute(
                """
                SELECT e.*, d.degree, d.specialization 
                FROM employees e
                JOIN doctors d ON e.id = d.id
                """
            )
            return await cursor.fetchall()


class Nurse:
    @staticmethod
    async def add(conn, employee_id, degree, password):
        async with conn.cursor() as cursor:
            await cursor.execute(
                """
                INSERT INTO nurses (id, degree, Employee_password)
                VALUES (%s, %s, %s)
                """,
                (employee_id, degree, password)
            )
            await conn.commit()

    @staticmethod
    async def get_all(conn):
        async with conn.cursor() as cursor:
            await cursor.execute(
                """
                SELECT e.*, n.degree
                FROM employees e
                JOIN nurses n ON e.id = n.id
                """
            )
            return await cursor.fetchall()


class Patient:
    @staticmethod
    async def add(conn, name, surname, age, blood_group, gender, contacts, next_of_keen, insurance, email, password):
        async with conn.cursor() as cursor:
            await cursor.execute(
                """
                INSERT INTO patients (patient_name, patient_surname, patient_age, patient_blood_group, gender, 
                contacts, next_of_keen_contacts, insurance, patient_email, password)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                """,
                (name, surname, age, blood_group, gender, contacts, next_of_keen, insurance, email, password)
            )
            await conn.commit()

    @staticmethod
    async def get_all(conn):
        async with conn.cursor() as cursor:
            await cursor.execute("SELECT * FROM patients")
            return await cursor.fetchall()


class Department:
    @staticmethod
    async def add(conn, department_name, employee_id):
        async with conn.cursor() as cursor:
            await cursor.execute(
                """
                INSERT INTO departments (department_name, id)
                VALUES (%s, %s)
                """,
                (department_name, employee_id)
            )
            await conn.commit()

    @staticmethod
    async def get_all(conn):
        async with conn.cursor() as cursor:
            await cursor.execute("SELECT * FROM departments")
            return await cursor.fetchall()
