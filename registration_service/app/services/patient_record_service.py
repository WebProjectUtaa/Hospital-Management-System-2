from app.db.models import Patient

class PatientRecordService:
    @staticmethod
    async def add_record(conn, patient_id, doctor_id, department_id, patient_status, doctor_note, prescription=None):
        query = """
        INSERT INTO patient_records (patient_id, id, department_id, patient_status, doctor_note, prescription)
        VALUES (%s, %s, %s, %s, %s, %s)
        """
        async with conn.cursor() as cur:
            await cur.execute(query, (patient_id, doctor_id, department_id, patient_status, doctor_note, prescription))
            await conn.commit()
        return {"message": "Patient record added successfully!"}

    @staticmethod
    async def update_record(conn, record_id, updates):
        update_fields = ", ".join([f"{key} = %s" for key in updates.keys()])
        query = f"""
        UPDATE patient_records
        SET {update_fields}
        WHERE record_id = %s
        """
        async with conn.cursor() as cur:
            await cur.execute(query, (*updates.values(), record_id))
            await conn.commit()
        return {"message": f"Patient record with ID {record_id} updated successfully!"}

    @staticmethod
    async def delete_record(conn, record_id):
        query = "DELETE FROM patient_records WHERE record_id = %s"
        async with conn.cursor() as cur:
            await cur.execute(query, (record_id,))
            await conn.commit()
        return {"message": f"Patient record with ID {record_id} deleted successfully!"}

    @staticmethod
    async def get_records_by_patient(conn, patient_id):
        query = """
        SELECT record_id, patient_id, id as doctor_id, department_id, patient_status, doctor_note, prescription
        FROM patient_records
        WHERE patient_id = %s
        """
        async with conn.cursor() as cur:
            await cur.execute(query, (patient_id,))
            records = await cur.fetchall()
            columns = ["record_id", "patient_id", "doctor_id", "department_id", "patient_status", "doctor_note", "prescription"]
            return [dict(zip(columns, row)) for row in records]

    @staticmethod
    async def get_records_by_doctor(conn, doctor_id):
        query = """
        SELECT record_id, patient_id, id as doctor_id, department_id, patient_status, doctor_note, prescription
        FROM patient_records
        WHERE id = %s
        """
        async with conn.cursor() as cur:
            await cur.execute(query, (doctor_id,))
            records = await cur.fetchall()
            columns = ["record_id", "patient_id", "doctor_id", "department_id", "patient_status", "doctor_note", "prescription"]
            return [dict(zip(columns, row)) for row in records]
