class Patient:
    @staticmethod
    async def add(conn, name, surname, age, blood_group, gender, contacts, next_of_keen_contacts, insurance, email, password):
        async with conn.cursor() as cursor:
            await cursor.execute("""
                INSERT INTO patients (patient_name, patient_surname, patient_age, patient_blood_group, gender, contacts, next_of_keen_contacts, insurance, patient_email, password)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            """, (name, surname, age, blood_group, gender, contacts, next_of_keen_contacts, insurance, email, password))
            await conn.commit()

    @staticmethod
    async def get_all(conn):
        async with conn.cursor() as cursor:
            await cursor.execute("SELECT * FROM patients")
            return await cursor.fetchall()

    @staticmethod
    async def update(conn, patient_id, name=None, surname=None, contacts=None):
        updates = []
        params = []

        if name:
            updates.append("patient_name = %s")
            params.append(name)
        if surname:
            updates.append("patient_surname = %s")
            params.append(surname)
        if contacts:
            updates.append("contacts = %s")
            params.append(contacts)

        params.append(patient_id)

        async with conn.cursor() as cursor:
            await cursor.execute(f"""
                UPDATE patients
                SET {', '.join(updates)}
                WHERE patient_id = %s
            """, tuple(params))
            await conn.commit()

    @staticmethod
    async def delete(conn, patient_id):
        async with conn.cursor() as cursor:
            await cursor.execute("DELETE FROM patients WHERE patient_id = %s", (patient_id,))
            await conn.commit()


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
