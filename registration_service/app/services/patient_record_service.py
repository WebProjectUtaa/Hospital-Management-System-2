from app.db.models import PatientRecord

class PatientRecordService:
    @staticmethod
    async def add_record(conn, patient_id, doctor_id, department_id, patient_status, doctor_note, prescription):
        await PatientRecord.add(conn, patient_id, doctor_id, department_id, patient_status, doctor_note, prescription)
        return {"message": "Patient record added successfully!"}

    @staticmethod
    async def get_records(conn, patient_id=None, doctor_id=None):
        return await PatientRecord.get_all(conn, patient_id, doctor_id)
