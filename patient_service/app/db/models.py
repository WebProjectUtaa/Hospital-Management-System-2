class PatientModel:
    @staticmethod
    async def get_patient_by_id(conn, patient_id):
        """
        Belirli bir hasta kaydını getir.
        """
        query = """
        SELECT * FROM patients
        WHERE patient_id = %s
        """
        async with conn.cursor() as cur:
            await cur.execute(query, (patient_id,))
            return await cur.fetchone()

    @staticmethod
    async def get_medical_history(conn, patient_id):
        """
        Hastanın tıbbi geçmişini getir.
        """
        query = """
        SELECT * FROM patient_records
        WHERE patient_id = %s
        """
        async with conn.cursor() as cur:
            await cur.execute(query, (patient_id,))
            return await cur.fetchall()

    @staticmethod
    async def get_lab_tests(conn, patient_id):
        """
        Hastanın laboratuvar testlerini getir.
        """
        query = """
        SELECT * FROM lab_tests
        WHERE patient_id = %s
        """
        async with conn.cursor() as cur:
            await cur.execute(query, (patient_id,))
            return await cur.fetchall()

    @staticmethod
    async def get_prescriptions(conn, patient_id):
        """
        Hastanın reçetelerini getir.
        """
        query = """
        SELECT * FROM prescriptions
        WHERE patient_id = %s
        """
        async with conn.cursor() as cur:
            await cur.execute(query, (patient_id,))
            return await cur.fetchall()
