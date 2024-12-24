class LoginModel:
    @staticmethod
    async def get_user_by_email(conn, email, role=None):
        query = """
        SELECT id, email, Employee_password AS password, role
        FROM employees
        WHERE email = %s
        """
        if role:
            query += " AND role = %s"

        async with conn.cursor() as cur:
            await cur.execute(query, (email, role) if role else (email,))
            return await cur.fetchone()

    @staticmethod
    async def get_patient_by_email(conn, email):
        query = """
        SELECT patient_id, patient_email AS email, password
        FROM patients
        WHERE patient_email = %s
        """
        async with conn.cursor() as cur:
            await cur.execute(query, (email,))
            return await cur.fetchone()
