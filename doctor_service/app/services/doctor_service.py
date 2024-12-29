from app.db.models import DoctorModel, PatientModel, AppointmentModel

class DoctorService:
    @staticmethod
    async def get_doctor_details(conn, doctor_id):
        """
        Retrieve doctor details by ID.
        """
        doctor = await DoctorModel.get_doctor_by_id(conn, doctor_id)
        if not doctor:
            raise ValueError(f"Doctor with ID {doctor_id} not found.")
        return doctor

    @staticmethod
    async def get_doctor_appointments(conn, doctor_id):
        """
        Retrieve all appointments for a doctor.
        """
        appointments = await DoctorModel.get_doctor_appointments(conn, doctor_id)
        return appointments

    @staticmethod
    async def update_doctor_availability(conn, doctor_id, availability_data):
        """
        Update a doctor's availability.
        """
        available_date = availability_data.get("available_date")
        available_start_time = availability_data.get("available_start_time")
        available_end_time = availability_data.get("available_end_time")
        is_available = availability_data.get("is_available", 1)

        if not (available_date and available_start_time and available_end_time):
            raise ValueError("Missing required fields for availability update.")

        await DoctorModel.update_doctor_availability(
            conn, doctor_id, available_date, available_start_time, available_end_time, is_available
        )
        return {"message": "Doctor availability updated successfully."}

    @staticmethod
    async def get_patient_medical_history(conn, patient_id):
        """
        Retrieve medical history of a patient for a doctor.
        """
        history = await PatientModel.get_patient_medical_history(conn, patient_id)
        if not history:
            raise ValueError(f"No medical history found for patient ID {patient_id}.")
        return history

    @staticmethod
    async def request_lab_test(conn, doctor_id, patient_id, test_data):
        """
        Request a lab test for a patient.
        """
        test_name = test_data.get("test_name")
        priority = test_data.get("priority", "low")

        if not test_name:
            raise ValueError("Test name is required.")

        await AppointmentModel.request_lab_test(conn, doctor_id, patient_id, test_name, priority)
        return {"message": "Lab test requested successfully."}

    @staticmethod
    async def prescribe_medication(conn, doctor_id, patient_id, medication_details):
        """
        Create a prescription for a patient.
        """
        if not medication_details:
            raise ValueError("Medication details are required.")

        await DoctorModel.create_prescription(conn, doctor_id, patient_id, medication_details)
        return {"message": "Prescription created successfully."}

    @staticmethod
    async def modify_appointment_schedule(conn, appointment_id, updated_data):
        """
        Modify an existing appointment schedule.
        """
        if not updated_data:
            raise ValueError("No data provided for appointment modification.")
        
        await AppointmentModel.update_appointment(conn, appointment_id, updated_data)
        return {"message": "Appointment schedule updated successfully."}

    @staticmethod
    async def cancel_appointment(conn, appointment_id):
        """
        Cancel an appointment.
        """
        await AppointmentModel.cancel_appointment(conn, appointment_id)
        return {"message": "Appointment canceled successfully."}

    @staticmethod
    async def manage_patient_notes(conn, patient_id, notes):
        """
        Add or update patient notes.
        """
        if not notes:
            raise ValueError("Notes are required.")
        
        await PatientModel.update_patient_notes(conn, patient_id, notes)
        return {"message": "Patient notes updated successfully."}
