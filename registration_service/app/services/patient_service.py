from app.db.models import Patient

class PatientService:
    @staticmethod
    async def add_patient(conn, name, surname, age, blood_group, gender, contacts, next_of_keen_contacts, insurance, email, password):
        await Patient.add(conn, name, surname, age, blood_group, gender, contacts, next_of_keen_contacts, insurance, email, password)
        return {"message": "Patient added successfully!"}

    @staticmethod
    async def get_all_patients(conn):
        return await Patient.get_all(conn)

    @staticmethod
    async def update_patient(conn, patient_id, name=None, surname=None, contacts=None):
        await Patient.update(conn, patient_id, name, surname, contacts)
        return {"message": f"Patient with ID {patient_id} updated successfully!"}

    @staticmethod
    async def delete_patient(conn, patient_id):
        await Patient.delete(conn, patient_id)
        return {"message": f"Patient with ID {patient_id} deleted successfully!"}
