class LabTest:
    table_name = "lab_tests"

    @staticmethod
    async def add(conn, patient_id, doctor_id, test_name, priority):
        query = """
        INSERT INTO lab_tests (patient_id, doctor_id, test_name, priority)
        VALUES (%s, %s, %s, %s)
        """
        await conn.execute(query, (patient_id, doctor_id, test_name, priority))

    @staticmethod
    async def get_all(conn):
        query = """
        SELECT test_id, patient_id, doctor_id, test_name, priority, status, result, requested_at, completed_at
        FROM lab_tests
        """
        async with conn.cursor() as cur:
            await cur.execute(query)
            rows = await cur.fetchall()
            return rows

    @staticmethod
    async def update_status(conn, test_id, status, result=None):
        query = """
        UPDATE lab_tests
        SET status = %s, result = %s, completed_at = CURRENT_TIMESTAMP
        WHERE test_id = %s
        """
        await conn.execute(query, (status, result, test_id))

    @staticmethod
    async def delete(conn, test_id):
        query = "DELETE FROM lab_tests WHERE test_id = %s"
        await conn.execute(query, (test_id,))