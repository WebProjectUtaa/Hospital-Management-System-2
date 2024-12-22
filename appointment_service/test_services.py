import asyncio
from app.db.init_db import init_db, get_db_connection, close_db
from app.services.appointment_service import AppointmentService
from app.services.doctoravailability_service import DoctorAvailabilityService


async def test_services():
    # Initialize DB connection pool
    await init_db()

    try:
        pool = await get_db_connection()
        async with pool.acquire() as conn:
            # Test Branches
            print("\nTesting Branches...")
            branches = await AppointmentService.get_branches(conn)
            print("Branches:", branches)

            # Test Available Doctors
            print("\nTesting Available Doctors...")
            branch_id = 1  # Example: Cardiology
            date = "2023-12-22"
            time = "09:00:00"
            available_doctors = await DoctorAvailabilityService.get_available_doctors(conn, branch_id, date, time)
            print("Available Doctors:", available_doctors)

            # Test Create Appointment
            print("\nTesting Create Appointment...")
            patient_id = 1  # Example patient
            doctor_id = 1  # Example doctor
            reason = "Routine check-up"
            appointment_result = await AppointmentService.create_appointment(conn, patient_id, doctor_id, date, time, reason)
            print("Appointment Creation Result:", appointment_result)

            # Test Get Appointments by Patient
            print("\nTesting Get Appointments by Patient...")
            appointments_by_patient = await AppointmentService.get_appointments_by_patient(conn, patient_id)
            print("Appointments by Patient:", appointments_by_patient)

            # Test Update Appointment Status
            print("\nTesting Update Appointment Status...")
            appointment_id = 1  # Example appointment ID
            new_status = "confirmed"
            update_status_result = await AppointmentService.update_appointment_status(conn, appointment_id, new_status)
            print("Update Appointment Status Result:", update_status_result)

            # Test Update Doctor Availability
            print("\nTesting Update Doctor Availability...")
            availability_update_result = await DoctorAvailabilityService.update_doctor_availability(conn, doctor_id, date, time, 0)
            print("Doctor Availability Update Result:", availability_update_result)

    except Exception as e:
        print("An error occurred during testing:", str(e))
    finally:
        # Close the connection pool
        await close_db()


if __name__ == "__main__":
    asyncio.run(test_services())
