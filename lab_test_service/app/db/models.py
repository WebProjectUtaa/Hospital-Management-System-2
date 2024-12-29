class LabTest:
    table_name = "lab_tests"

    @staticmethod
    async def add(conn, patient_id, doctor_id, test_name, priority):
        """
        Yeni laboratuvar testi ekler.
        """
        query = """
        INSERT INTO lab_tests (patient_id, doctor_id, test_name, priority)
        VALUES (%s, %s, %s, %s)
        """
        async with conn.cursor() as cur:
            await cur.execute(query, (patient_id, doctor_id, test_name, priority))
            await conn.commit()

    @staticmethod
    async def get_all(conn):
        """
        Tüm laboratuvar testlerini döner.
        """
        query = """
        SELECT test_id, patient_id, doctor_id, test_name, priority, status, result, requested_at, completed_at
        FROM lab_tests
        """
        async with conn.cursor() as cur:
            await cur.execute(query)
            rows = await cur.fetchall()
            return rows

    @staticmethod
    async def get_by_staff(conn, staff_id):
        """
        Belirli bir laboratuvar personeline atanmış testleri döner.
        """
        query = """
        SELECT test_id, patient_id, doctor_id, test_name, priority, status, result, requested_at, completed_at
        FROM lab_tests
        WHERE assigned_staff_id = %s
        """
        async with conn.cursor() as cur:
            await cur.execute(query, (staff_id,))
            rows = await cur.fetchall()
            return rows

    @staticmethod
    async def get_by_doctor(conn, doctor_id):
        """
        Belirli bir doktorun talep ettiği testleri döner.
        """
        query = """
        SELECT test_id, patient_id, test_name, priority, status, result, requested_at, completed_at
        FROM lab_tests
        WHERE doctor_id = %s
        """
        async with conn.cursor() as cur:
            await cur.execute(query, (doctor_id,))
            rows = await cur.fetchall()
            return rows

    @staticmethod
    async def get_by_patient(conn, patient_id):
        """
        Belirli bir hastanın testlerini döner.
        """
        query = """
        SELECT test_id, doctor_id, test_name, priority, status, result, requested_at, completed_at
        FROM lab_tests
        WHERE patient_id = %s
        """
        async with conn.cursor() as cur:
            await cur.execute(query, (patient_id,))
            rows = await cur.fetchall()
            return rows

    @staticmethod
    async def assign_staff(conn, test_id, staff_id):
        """
        Laboratuvar testini bir personele atar.
        """
        query = """
        UPDATE lab_tests
        SET assigned_staff_id = %s, assigned_at = CURRENT_TIMESTAMP
        WHERE test_id = %s
        """
        async with conn.cursor() as cur:
            await cur.execute(query, (staff_id, test_id))
            await conn.commit()

    @staticmethod
    async def update_status(conn, test_id, status, result=None):
        """
        Laboratuvar testinin durumunu günceller.
        """
        query = """
        UPDATE lab_tests
        SET status = %s, result = %s, completed_at = CURRENT_TIMESTAMP
        WHERE test_id = %s
        """
        async with conn.cursor() as cur:
            await cur.execute(query, (status, result, test_id))
            await conn.commit()

    @staticmethod
    async def delete(conn, test_id):
        """
        Laboratuvar testini siler.
        """
        query = "DELETE FROM lab_tests WHERE test_id = %s"
        async with conn.cursor() as cur:
            await cur.execute(query, (test_id,))
            await conn.commit()
