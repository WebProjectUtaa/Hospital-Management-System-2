class AuthModel:
    @staticmethod
    async def get_employee_by_email(conn, email):
        query = """
        SELECT id, email, Employee_password AS password, role
        FROM employees
        WHERE email = %s
        """
        async with conn.cursor() as cur:
            await cur.execute(query, (email,))
            return await cur.fetchone()

    @staticmethod
    async def get_patient_by_email(conn, email):
        query = """
        SELECT patient_id AS id, patient_email AS email, password
        FROM patients
        WHERE patient_email = %s
        """
        async with conn.cursor() as cur:
            await cur.execute(query, (email,))
            return await cur.fetchone()
