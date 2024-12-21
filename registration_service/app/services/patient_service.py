from app.db.models import Patient

class PatientService:
    @staticmethod
    async def add_patient(conn, name, surname, age, blood_group, gender, contacts, next_of_keen, insurance, email, password, current_user_role="receptionist"):
        if current_user_role not in ["receptionist", "admin"]:
            raise ValueError("Unauthorized: Only receptionist or admin can add patients.")

        await Patient.add(conn, name, surname, age, blood_group, gender, contacts, next_of_keen, insurance, email, password)
        return {"message": f"Patient {name} {surname} added successfully!"}

    @staticmethod
    async def get_all_patients(conn):
        patients = await Patient.get_all(conn)
        return patients

    @staticmethod
    async def update_patient(conn, patient_id, name=None, surname=None, contacts=None):
        if not (name or surname or contacts):
            raise ValueError("At least one field (name, surname, contacts) must be provided to update.")

        await Patient.update(conn, patient_id, name, surname, contacts)
        return {"message": f"Patient with ID {patient_id} updated successfully!"}

    @staticmethod
    async def delete_patient(conn, patient_id):
        await Patient.delete(conn, patient_id)
        return {"message": f"Patient with ID {patient_id} deleted successfully!"}
