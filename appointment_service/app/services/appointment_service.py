from app.db.models import Appointment, DoctorAvailability

class AppointmentService:
    @staticmethod
    async def get_branches(conn):
        query = "SELECT branch_id, branch_name FROM branches"
        async with conn.cursor() as cur:
            await cur.execute(query)
            return await cur.fetchall()

    @staticmethod
    async def get_available_doctors(conn, branch_id, date, time):
        return await DoctorAvailability.get_available_doctors(conn, branch_id, date, time)

    @staticmethod
    async def create_appointment(conn, patient_id, doctor_id, date, time, reason):
        # Çakışma kontrolü
        query = """
        SELECT COUNT(*) 
        FROM appointments 
        WHERE doctor_id = %s AND appointment_date = %s AND appointment_time = %s
         """
        async with conn.cursor() as cur:
            await cur.execute(query, (doctor_id, date, time))
            count = await cur.fetchone()
            if count[0] > 0:
                raise ValueError("The doctor is already booked for the selected date and time.")

        # Randevu oluşturma
        await Appointment.add(conn, patient_id, doctor_id, date, time, reason)
        await DoctorAvailability.update_availability(conn, doctor_id, date, time, 0)
        return {"message": "Appointment successfully created."}


    @staticmethod
    async def get_appointments_by_patient(conn, patient_id):
        return await Appointment.get_by_patient(conn, patient_id)

    @staticmethod
    async def update_appointment_status(conn, appointment_id, status):
        await Appointment.update_status(conn, appointment_id, status)
        return {"message": f"Appointment ID {appointment_id} status updated to {status}."}
