class Employee:
    table_name = "employees"

    @staticmethod
    async def add(conn, name, surname, email, gender, contacts, department):
        query = """
        INSERT INTO employees (Employee_name, surname, email, gender, contacts, department)
        VALUES (%s, %s, %s, %s, %s, %s)
        """
        await conn.execute(query, (name, surname, email, gender, contacts, department))

    @staticmethod
    async def get_all(conn):
        query = """
        SELECT id, Employee_name, surname, email, gender, contacts, department
        FROM employees
        """
        async with conn.cursor() as cur:
            await cur.execute(query)
            rows = await cur.fetchall()
            return rows

    @staticmethod
    async def delete(conn, employee_id):
        query = "DELETE FROM employees WHERE id = %s"
        await conn.execute(query, (employee_id,))


class Patient:
    table_name = "patients"

    @staticmethod
    async def add(conn, name, surname, age, blood_group, gender, contacts, keen_contacts, insurance, email, password):
        query = """
        INSERT INTO patients (patient_name, patient_surname, patient_age, patient_blood_group, Gender, contacts,
                              next_of_keen_contacts, insurance, patient_email, password)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """
        await conn.execute(query, (name, surname, age, blood_group, gender, contacts, keen_contacts, insurance, email, password))

    @staticmethod
    async def get_all(conn):
        query = """
        SELECT patient_id, patient_name, patient_surname, patient_age, patient_blood_group, Gender, contacts, 
               next_of_keen_contacts, insurance, patient_email
        FROM patients
        """
        async with conn.cursor() as cur:
            await cur.execute(query)
            rows = await cur.fetchall()
            return rows

    @staticmethod
    async def delete(conn, patient_id):
        query = "DELETE FROM patients WHERE patient_id = %s"
        await conn.execute(query, (patient_id,))


class Doctor:
    table_name = "doctors"

    @staticmethod
    async def add(conn, id, degree, specialization, password):
        query = """
        INSERT INTO doctors (id, degree, specialization, Employee_password)
        VALUES (%s, %s, %s, %s)
        """
        await conn.execute(query, (id, degree, specialization, password))

    @staticmethod
    async def get_all(conn):
        query = """
        SELECT d.id, e.Employee_name, e.surname, e.email, e.gender, e.contacts, e.department, d.degree, d.specialization
        FROM doctors d
        INNER JOIN employees e ON d.id = e.id
        """
        async with conn.cursor() as cur:
            await cur.execute(query)
            rows = await cur.fetchall()
            return rows


class Nurse:
    table_name = "nurses"

    @staticmethod
    async def add(conn, id, degree, password):
        query = """
        INSERT INTO nurses (id, degree, Employee_password)
        VALUES (%s, %s, %s)
        """
        await conn.execute(query, (id, degree, password))

    @staticmethod
    async def get_all(conn):
        query = """
        SELECT n.id, e.Employee_name, e.surname, e.email, e.gender, e.contacts, e.department, n.degree
        FROM nurses n
        INNER JOIN employees e ON n.id = e.id
        """
        async with conn.cursor() as cur:
            await cur.execute(query)
            rows = await cur.fetchall()
            return rows


class Department:
    table_name = "departments"

    @staticmethod
    async def add(conn, department_id, department_name, employee_id):
        query = """
        INSERT INTO departments (department_id, department_name, id)
        VALUES (%s, %s, %s)
        """
        await conn.execute(query, (department_id, department_name, employee_id))

    @staticmethod
    async def get_all(conn):
        query = """
        SELECT department_id, department_name, id
        FROM departments
        """
        async with conn.cursor() as cur:
            await cur.execute(query)
            rows = await cur.fetchall()
            return rows

class PatientRecord:
    table_name = "patient_records"

    @staticmethod
    async def add(conn, patient_id, doctor_id, department_id, patient_status, doctor_note, prescription=None):
        query = """
        INSERT INTO patient_records (patient_id, id, department_id, patient_status, doctor_note, prescription)
        VALUES (%s, %s, %s, %s, %s, %s)
        """
        await conn.execute(query, (patient_id, doctor_id, department_id, patient_status, doctor_note, prescription))

    @staticmethod
    async def update(conn, record_id, updates):
        update_fields = ", ".join([f"{key} = %s" for key in updates.keys()])
        query = f"""
        UPDATE patient_records
        SET {update_fields}
        WHERE record_id = %s
        """
        await conn.execute(query, (*updates.values(), record_id))

    @staticmethod
    async def delete(conn, record_id):
        query = "DELETE FROM patient_records WHERE record_id = %s"
        await conn.execute(query, (record_id,))

    @staticmethod
    async def get_by_patient(conn, patient_id):
        query = """
        SELECT record_id, patient_id, id as doctor_id, department_id, patient_status, doctor_note, prescription
        FROM patient_records
        WHERE patient_id = %s
        """
        async with conn.cursor() as cur:
            await cur.execute(query, (patient_id,))
            rows = await cur.fetchall()
            columns = ["record_id", "patient_id", "doctor_id", "department_id", "patient_status", "doctor_note", "prescription"]
            return [dict(zip(columns, row)) for row in rows]

    @staticmethod
    async def get_by_doctor(conn, doctor_id):
        query = """
        SELECT record_id, patient_id, id as doctor_id, department_id, patient_status, doctor_note, prescription
        FROM patient_records
        WHERE id = %s
        """
        async with conn.cursor() as cur:
            await cur.execute(query, (doctor_id,))
            rows = await cur.fetchall()
            columns = ["record_id", "patient_id", "doctor_id", "department_id", "patient_status", "doctor_note", "prescription"]
            return [dict(zip(columns, row)) for row in rows]
