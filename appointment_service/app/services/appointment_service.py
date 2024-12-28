import requests
from app.db.models import Appointment
from app.services.doctoravailability_service import DoctorAvailabilityService


class AppointmentService:
    @staticmethod
    async def create_appointment(conn, patient_id, doctor_id, date, time, reason):
        """
        Create an appointment and notify the patient and doctor.
        """
        # Fetch patient and doctor information
        patient_info = await AppointmentService.fetch_patient_info(patient_id)
        doctor_info = await AppointmentService.fetch_doctor_info(doctor_id)

        if not patient_info or not doctor_info:
            raise ValueError("Invalid patient or doctor ID provided.")

        # Check for conflicting appointments
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

        # Add the appointment
        await Appointment.add(conn, patient_id, doctor_id, date, time, reason)
        await DoctorAvailabilityService.update_doctor_availability(conn, doctor_id, date, time, is_available=0)

        # Send notifications to the patient and doctor
        await AppointmentService.send_notifications(patient_info, doctor_info, date, time, reason)

        return {"message": "Appointment successfully created and notifications sent."}

    @staticmethod
    async def fetch_patient_info(patient_id):
        """
        Fetch patient information from Registration Service.
        """
        try:
            response = requests.get(f"http://localhost:8001/patients/{patient_id}")
            if response.status_code == 200:
                return response.json()
        except Exception as e:
            print(f"Error fetching patient info: {e}")
        return None

    @staticmethod
    async def fetch_doctor_info(doctor_id):
        """
        Fetch doctor information from Registration Service.
        """
        try:
            response = requests.get(f"http://localhost:8001/employees/{doctor_id}")
            if response.status_code == 200:
                return response.json()
        except Exception as e:
            print(f"Error fetching doctor info: {e}")
        return None

    @staticmethod
    async def send_notifications(patient, doctor, date, time, reason):
        """
        Send notifications to the patient and doctor using Notification Service.
        """
        try:
            patient_notification = {
                "to_email": patient["email"],
                "subject": "Appointment Confirmation",
                "message": f"""
                Dear {patient['name']},

                Your appointment has been successfully created with the following details:
                - Date: {date}
                - Time: {time}
                - Doctor: {doctor['name']}
                - Reason: {reason}

                Best regards,
                Hospital Management System
                """
            }
            doctor_notification = {
                "to_email": doctor["email"],
                "subject": "New Appointment Scheduled",
                "message": f"""
                Dear Dr. {doctor['name']},

                A new appointment has been scheduled:
                - Patient: {patient['name']}
                - Date: {date}
                - Time: {time}
                - Reason: {reason}

                Best regards,
                Hospital Management System
                """
            }
            requests.post("http://localhost:8000/notifications", json=patient_notification)
            requests.post("http://localhost:8000/notifications", json=doctor_notification)
        except Exception as e:
            print(f"Notification Service error: {e}")

    @staticmethod
    async def cancel_appointment(conn, appointment_id):
        """
        Cancel an appointment and notify the patient and doctor.
        """
        # Fetch appointment information
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

        # Delete the appointment
        query = "DELETE FROM appointments WHERE appointment_id = %s"
        async with conn.cursor() as cur:
            await cur.execute(query, (appointment_id,))
            await conn.commit()

        # Send notifications about the cancellation
        try:
            patient_notification = {
                "to_email": appointment["patient_email"],
                "subject": "Appointment Cancellation",
                "message": f"""
                Dear {appointment['patient_name']},

                Your appointment scheduled for {appointment['appointment_date']} at {appointment['appointment_time']} has been canceled.

                Best regards,
                Hospital Management System
                """
            }
            doctor_notification = {
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
            requests.post("http://localhost:8000/notifications", json=patient_notification)
            requests.post("http://localhost:8000/notifications", json=doctor_notification)
        except Exception as e:
            print(f"Notification Service error: {e}")

        return {"message": "Appointment successfully canceled and notifications sent."}
