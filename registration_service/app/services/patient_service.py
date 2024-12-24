from app.db.models import Patient
from utils.hash_utils import HashUtils

class PatientService:
    @staticmethod
    async def add_patient(conn, name, surname, age, blood_group, gender, contacts, keen_contacts, insurance, email, password):
        hashed_password = HashUtils.hash_password(password)  # Güncellendi
        await Patient.add(conn, name, surname, age, blood_group, gender, contacts, keen_contacts, insurance, email, hashed_password)
        return {"message": f"Patient '{name} {surname}' added successfully!"}

    @staticmethod
    async def update_patient(conn, patient_id, updates):
        if "password" in updates:
            updates["password"] = HashUtils.hash_password(updates["password"])  # Güncellendi

        update_fields = ", ".join([f"{key} = %s" for key in updates.keys()])
        query = f"""
        UPDATE patients
        SET {update_fields}
        WHERE patient_id = %s
        """
        async with conn.cursor() as cur:
            await cur.execute(query, (*updates.values(), patient_id))
            await conn.commit()
        return {"message": f"Patient with ID {patient_id} updated successfully!"}
