from app.db.models import Appointment
from app.services.doctoravailability_service import DoctorAvailabilityService
from app.utils.email_sender import EmailSender


class AppointmentService:
    @staticmethod
    async def create_appointment(conn, patient_id, doctor_id, date, time, reason):
        try:
            # Çakışma kontrolü
            query = """
            SELECT COUNT(*) AS conflict_count
            FROM appointments 
            WHERE doctor_id = %s AND appointment_date = %s AND appointment_time = %s
            """
            async with conn.cursor() as cur:
                print(f"Checking appointment conflicts for doctor_id={doctor_id}, date={date}, time={time}")
                await cur.execute(query, (doctor_id, date, time))
                count = await cur.fetchone()
                print(f"Raw Conflict Check Result: {count}")
                
                if not count or count["conflict_count"] > 0:
                    raise ValueError("The doctor is already booked for the selected date and time.")

            # Randevu oluşturma
            print(f"Creating appointment for patient_id={patient_id}, doctor_id={doctor_id}")
            await Appointment.add(conn, patient_id, doctor_id, date, time, reason)
            await DoctorAvailabilityService.update_doctor_availability(conn, doctor_id, date, time, 0)
            print("Appointment created successfully.")

            # Hasta ve doktor bilgilerini al
            patient_query = "SELECT patient_name, patient_email FROM patients WHERE patient_id = %s"
            doctor_query = """
            SELECT e.Employee_name, e.email
            FROM doctors d
            INNER JOIN employees e ON d.id = e.id
            WHERE d.id = %s
            """
            async with conn.cursor() as cur:
                await cur.execute(patient_query, (patient_id,))
                patient = await cur.fetchone()
                print("Patient Info:", patient)

                await cur.execute(doctor_query, (doctor_id,))
                doctor = await cur.fetchone()
                print("Doctor Info:", doctor)

            # Hasta e-postası
            patient_message = f"""
            Dear {patient['patient_name']},

            Your appointment has been successfully created with the following details:
            - Date: {date}
            - Time: {time}
            - Doctor: {doctor['Employee_name']}
            - Reason: {reason}

            Best regards,
            Hospital Management System
            """
            EmailSender.send_email(patient["patient_email"], "Appointment Confirmation", patient_message)

            # Doktor e-postası
            doctor_message = f"""
            Dear Dr. {doctor['Employee_name']},

            A new appointment has been scheduled:
            - Patient: {patient['patient_name']}
            - Date: {date}
            - Time: {time}
            - Reason: {reason}

            Best regards,
            Hospital Management System
            """
            EmailSender.send_email(doctor["email"], "New Appointment Scheduled", doctor_message)

            return {"message": "Appointment successfully created and emails sent to patient and doctor."}
        except Exception as e:
            print(f"Error in create_appointment: {e}")
            raise



    @staticmethod
    async def cancel_appointment(conn, appointment_id):
        """
        Randevuyu iptal eder ve hasta ile doktora e-posta gönderir.
        """
        # İlgili hasta ve doktor bilgilerini al
        appointment_query = """
        SELECT 
            p.patient_email, p.patient_name, 
            a.appointment_date, a.appointment_time, 
            e.email AS doctor_email, e.Employee_name AS doctor_name
        FROM appointments a
        INNER JOIN patients p ON a.patient_id = p.patient_id
        INNER JOIN doctors d ON a.doctor_id = d.id
        INNER JOIN employees e ON d.id = e.id
        WHERE a.appointment_id = %s
        """
        async with conn.cursor() as cur:
            await cur.execute(appointment_query, (appointment_id,))
            appointment = await cur.fetchone()

        if not appointment:
            raise ValueError("Appointment not found.")

        # Randevuyu iptal et
        query = "DELETE FROM appointments WHERE appointment_id = %s"
        async with conn.cursor() as cur:
            await cur.execute(query, (appointment_id,))
            await conn.commit()

        # Hasta e-postası
        patient_message = f"""
        Dear {appointment['patient_name']},

        Your appointment scheduled for {appointment['appointment_date']} at {appointment['appointment_time']} has been canceled.

        Best regards,
        Hospital Management System
        """
        EmailSender.send_email(appointment["patient_email"], "Appointment Cancellation", patient_message)

        # Doktor e-postası
        doctor_message = f"""
        Dear Dr. {appointment['doctor_name']},

        The appointment scheduled with the following details has been canceled:
        - Patient: {appointment['patient_name']}
        - Date: {appointment['appointment_date']}
        - Time: {appointment['appointment_time']}

        Please update your schedule accordingly.

        Best regards,
        Hospital Management System
        """
        EmailSender.send_email(appointment["doctor_email"], "Appointment Cancellation Notification", doctor_message)

        return {"message": "Appointment successfully canceled and notification emails sent."}
