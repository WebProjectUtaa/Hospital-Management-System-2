class DoctorModel:
    @staticmethod
    async def get_doctor_by_id(conn, doctor_id):
        """
        Verilen ID'ye göre doktor bilgilerini alır.
        """
        query = """
        SELECT d.id, e.Employee_name AS name, e.surname, d.degree, d.specialization, e.email, e.contacts
        FROM doctors d
        INNER JOIN employees e ON d.employee_id = e.id
        WHERE d.id = %s
        """
        async with conn.cursor() as cur:
            await cur.execute(query, (doctor_id,))
            return await cur.fetchone()

    @staticmethod
    async def get_doctor_appointments(conn, doctor_id):
        """
        Doktorun randevularını alır.
        """
        query = """
        SELECT a.appointment_id, a.patient_id, a.appointment_date, a.appointment_time, a.reason, a.status
        FROM appointments a
        WHERE a.doctor_id = %s
        ORDER BY a.appointment_date, a.appointment_time
        """
        async with conn.cursor() as cur:
            await cur.execute(query, (doctor_id,))
            return await cur.fetchall()

    @staticmethod
    async def update_doctor_availability(conn, doctor_id, available_date, available_time, is_available):
        """
        Doktorun belirli bir tarih ve saat için uygunluk durumunu günceller.
        """
        query = """
        UPDATE doctor_availability
        SET is_available = %s
        WHERE doctor_id = %s AND available_date = %s AND available_time = %s
        """
        async with conn.cursor() as cur:
            await cur.execute(query, (is_available, doctor_id, available_date, available_time))
            await conn.commit()

    @staticmethod
    async def get_doctor_availability(conn, doctor_id):
        """
        Doktorun mevcut uygunluk durumunu alır.
        """
        query = """
        SELECT available_date, available_time, is_available
        FROM doctor_availability
        WHERE doctor_id = %s
        ORDER BY available_date, available_time
        """
        async with conn.cursor() as cur:
            await cur.execute(query, (doctor_id,))
            return await cur.fetchall()

class AppointmentModel:
    @staticmethod
    async def update_appointment(conn, appointment_id, updated_data):
        """
        Update an appointment's details.
        """
        update_fields = ", ".join([f"{key} = %s" for key in updated_data.keys()])
        query = f"""
        UPDATE appointments
        SET {update_fields}
        WHERE appointment_id = %s
        """
        async with conn.cursor() as cur:
            await cur.execute(query, (*updated_data.values(), appointment_id))
            await conn.commit()

    @staticmethod
    async def cancel_appointment(conn, appointment_id):
        """
        Cancel an appointment.
        """
        query = """
        UPDATE appointments
        SET status = 'canceled'
        WHERE appointment_id = %s
        """
        async with conn.cursor() as cur:
            await cur.execute(query, (appointment_id,))
            await conn.commit()

class PatientModel:
    @staticmethod
    async def update_patient_notes(conn, patient_id, notes):
        """
        Update notes for a specific patient.
        """
        query = """
        UPDATE patient_records
        SET doctor_note = %s
        WHERE patient_id = %s
        """
        async with conn.cursor() as cur:
            await cur.execute(query, (notes, patient_id))
            await conn.commit()
