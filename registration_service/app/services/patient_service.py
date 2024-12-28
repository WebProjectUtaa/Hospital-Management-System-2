import bcrypt
from app.db.models import Patient

class PatientService:
    @staticmethod
    async def add_patient(conn, name, surname, age, blood_group, gender, contacts, keen_contacts, insurance, email, password):
        """
        Yeni hasta eklemek için metod.
        """
        hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
        async with conn.cursor() as cur:
            await cur.execute("""
                INSERT INTO patients (
                    patient_name, patient_surname, patient_age, patient_blood_group, gender, contacts, next_of_keen_contacts, insurance, patient_email, password
                ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            """, (name, surname, age, blood_group, gender, contacts, keen_contacts, insurance, email, hashed_password))
            await conn.commit()
        return {"message": f"Patient '{name} {surname}' added successfully!"}

    @staticmethod
    async def update_patient(conn, patient_id, updates):
        """
        Hasta bilgilerini güncellemek için metod.
        """
        if "password" in updates:
            updates["password"] = bcrypt.hashpw(updates["password"].encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
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
    async def get_all_patients(conn):
        """
        Tüm hastaları listelemek için metod.
        """
        async with conn.cursor() as cur:
            await cur.execute("SELECT * FROM patients")
            patients = await cur.fetchall()
        return patients

    @staticmethod
    async def delete_patient(conn, patient_id):
        """
        Hasta kaydını silmek için metod.
        """
        async with conn.cursor() as cur:
            await cur.execute("DELETE FROM patients WHERE patient_id = %s", (patient_id,))
            await conn.commit()
        return {"message": f"Patient with ID {patient_id} deleted successfully!"}
