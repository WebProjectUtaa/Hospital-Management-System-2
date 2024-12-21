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

class PatientRecord:
    @staticmethod
    async def add(conn, patient_id, doctor_id, department_id, patient_status, doctor_note, prescription):
        async with conn.cursor() as cursor:
            await cursor.execute("""
                INSERT INTO patient_records (patient_id, id, department_id, patient_status, doctor_note, prescription)
                VALUES (%s, %s, %s, %s, %s, %s)
            """, (patient_id, doctor_id, department_id, patient_status, doctor_note, prescription))
            await conn.commit()

    @staticmethod
    async def get_all(conn, patient_id=None, doctor_id=None):
        query = "SELECT * FROM patient_records WHERE 1=1"
        params = []

        if patient_id:
            query += " AND patient_id = %s"
            params.append(patient_id)
        if doctor_id:
            query += " AND id = %s"
            params.append(doctor_id)

        async with conn.cursor() as cursor:
            await cursor.execute(query, tuple(params))
            return await cursor.fetchall()

    @staticmethod
    async def update(conn, record_id, patient_status=None, doctor_note=None, prescription=None):
        updates = []
        params = []

        if patient_status:
            updates.append("patient_status = %s")
            params.append(patient_status)
        if doctor_note:
            updates.append("doctor_note = %s")
            params.append(doctor_note)
        if prescription:
            updates.append("prescription = %s")
            params.append(prescription)

        params.append(record_id)

        async with conn.cursor() as cursor:
            await cursor.execute(f"""
                UPDATE patient_records
                SET {', '.join(updates)}
                WHERE record_id = %s
            """, tuple(params))
            await conn.commit()

    @staticmethod
    async def delete(conn, record_id):
        async with conn.cursor() as cursor:
            await cursor.execute("DELETE FROM patient_records WHERE record_id = %s", (record_id,))
            await conn.commit()