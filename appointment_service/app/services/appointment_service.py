import requests
from app.db.models import Appointment
from app.services.doctoravailability_service import DoctorAvailabilityService

class AppointmentService:
    @staticmethod
    async def create_appointment(conn, patient_id, doctor_id, date, time, reason):
        """
        Randevu oluşturma ve Notification Service ile entegrasyon.
        """
        # Çakışma kontrolü
        query = """
        SELECT COUNT(*) 
        FROM appointments 
        WHERE doctor_id = %s AND appointment_date = %s AND appointment_time = %s
        """
        async with conn.cursor() as cur:
            await cur.execute(query, (doctor_id, date, time))
            count = await cur.fetchone()
            if count["COUNT(*)"] > 0:
                raise ValueError("The doctor is already booked for the selected date and time.")

        # Randevuyu ekle
        await Appointment.add(conn, patient_id, doctor_id, date, time, reason)
        await DoctorAvailabilityService.update_doctor_availability(conn, doctor_id, date, time, is_available=0)

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

            await cur.execute(doctor_query, (doctor_id,))
            doctor = await cur.fetchone()

        # Notification Service API çağrıları
        try:
            notification_data_patient = {
                "to_email": patient["patient_email"],
                "subject": "Appointment Confirmation",
                "message": f"""
                Dear {patient['patient_name']},

                Your appointment has been successfully created with the following details:
                - Date: {date}
                - Time: {time}
                - Doctor: {doctor['Employee_name']}
                - Reason: {reason}

                Best regards,
                Hospital Management System
                """
            }
            notification_data_doctor = {
                "to_email": doctor["email"],
                "subject": "New Appointment Scheduled",
                "message": f"""
                Dear Dr. {doctor['Employee_name']},

                A new appointment has been scheduled:
                - Patient: {patient['patient_name']}
                - Date: {date}
                - Time: {time}
                - Reason: {reason}

                Best regards,
                Hospital Management System
                """
            }
            # Notification Service'e REST istekleri
            requests.post("http://localhost:8000/notifications/send_email", json=notification_data_patient)
            requests.post("http://localhost:8000/notifications/send_email", json=notification_data_doctor)
        except Exception as e:
            print(f"Notification Service error: {e}")

        return {"message": "Appointment successfully created and notifications sent."}

    @staticmethod
    async def cancel_appointment(conn, appointment_id):
        """
        Randevuyu iptal etme ve Notification Service ile entegrasyon.
        """
        # Randevu bilgilerini al
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

        # Randevuyu sil
        query = "DELETE FROM appointments WHERE appointment_id = %s"
        async with conn.cursor() as cur:
            await cur.execute(query, (appointment_id,))
            await conn.commit()

        # Notification Service API çağrıları
        try:
            notification_data_patient = {
                "to_email": appointment["patient_email"],
                "subject": "Appointment Cancellation",
                "message": f"""
                Dear {appointment['patient_name']},

                Your appointment scheduled for {appointment['appointment_date']} at {appointment['appointment_time']} has been canceled.

                Best regards,
                Hospital Management System
                """
            }
            notification_data_doctor = {
                "to_email": appointment["doctor_email"],
                "subject": "Appointment Cancellation Notification",
                "message": f"""
                Dear Dr. {appointment['doctor_name']},

                The appointment scheduled with the following details has been canceled:
                - Patient: {appointment['patient_name']}
                - Date: {appointment['appointment_date']}
                - Time: {appointment['appointment_time']}

                Best regards,
                Hospital Management System
                """
            }
            # Notification Service'e REST istekleri
            requests.post("http://localhost:8000/notifications/send_email", json=notification_data_patient)
            requests.post("http://localhost:8000/notifications/send_email", json=notification_data_doctor)
        except Exception as e:
            print(f"Notification Service error: {e}")

        return {"message": "Appointment successfully canceled and notifications sent."}
