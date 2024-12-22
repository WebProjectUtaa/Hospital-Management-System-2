from app.db.models import Patient
from app.utils.security import hash_password

class PatientService:
    @staticmethod
    async def add_patient(conn, name, surname, age, blood_group, gender, contacts, keen_contacts, insurance, email, password):
        hashed_password = hash_password(password) 
        await Patient.add(conn, name, surname, age, blood_group, gender, contacts, keen_contacts, insurance, email, hashed_password)
        return {"message": f"Patient '{name} {surname}' added successfully!"}

    @staticmethod
    async def update_patient(conn, patient_id, updates):
        if "password" in updates:
            updates["password"] = hash_password(updates["password"]) 

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

    @staticmethod
    async def update_patient(conn, patient_id, updates):
        if "password" in updates:
            updates["password"] = hash_password(updates["password"])

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



    @staticmethod
    async def delete_patient(conn, patient_id):
        query = "DELETE FROM patients WHERE patient_id = %s"
        async with conn.cursor() as cur:
            await cur.execute(query, (patient_id,))
            await conn.commit()
        return {"message": f"Patient with ID {patient_id} deleted successfully!"}

    @staticmethod
    async def get_all_patients(conn):
        return await Patient.get_all(conn)

    @staticmethod
    async def get_patient_by_id(conn, patient_id):
        query = """
        SELECT patient_id, patient_name, patient_surname, patient_age, patient_blood_group, Gender, contacts, 
               next_of_keen_contacts, insurance, patient_email
        FROM patients
        WHERE patient_id = %s
        """
        async with conn.cursor() as cur:
            await cur.execute(query, (patient_id,))
            patient = await cur.fetchone()

            if not patient:
                return {"error": f"Patient with ID {patient_id} not found."}, 404

            columns = ["patient_id", "patient_name", "patient_surname", "patient_age", "patient_blood_group", 
                       "Gender", "contacts", "next_of_keen_contacts", "insurance", "patient_email"]
            return dict(zip(columns, patient))
