class Nurse:
    @staticmethod
    async def assign_patient(conn, nurse_id, patient_id):
        query = """
        INSERT INTO nurse_patient_assignments (nurse_id, patient_id, assigned_at)
        VALUES (%s, %s, CURRENT_TIMESTAMP)
        """
        async with conn.cursor() as cur:
            await cur.execute(query, (nurse_id, patient_id))
            await conn.commit()

    @staticmethod
    async def get_assigned_patients(conn, nurse_id):
        query = """
        SELECT p.patient_id, p.patient_name, p.patient_surname, p.patient_age, p.patient_blood_group, p.gender
        FROM patients p
        INNER JOIN nurse_patient_assignments npa ON p.patient_id = npa.patient_id
        WHERE npa.nurse_id = %s
        """
        async with conn.cursor() as cur:
            await cur.execute(query, (nurse_id,))
            return await cur.fetchall()

    @staticmethod
    async def update_patient_status(conn, patient_id, status):
        query = """
        UPDATE patients
        SET status = %s
        WHERE patient_id = %s
        """
        async with conn.cursor() as cur:
            await cur.execute(query, (status, patient_id))
            await conn.commit()

    @staticmethod
    async def get_assigned_lab_tests(conn, nurse_id):
        query = """
        SELECT lt.test_id, lt.test_name, lt.priority, lt.status, lt.result
        FROM lab_tests lt
        INNER JOIN nurse_patient_assignments npa ON lt.patient_id = npa.patient_id
        WHERE npa.nurse_id = %s
        """
        async with conn.cursor() as cur:
            await cur.execute(query, (nurse_id,))
            return await cur.fetchall()
