from app.db.models import DoctorAvailability


class DoctorAvailabilityService:
    @staticmethod
    async def get_available_doctors(conn, branch_id, date, time):
        return await DoctorAvailability.get_available_doctors(conn, branch_id, date, time)

    @staticmethod
    async def update_doctor_availability(conn, doctor_id, date, time, is_available):
        await DoctorAvailability.update_availability(conn, doctor_id, date, time, is_available)
        return {"message": f"Doctor availability updated for doctor_id={doctor_id} on {date} at {time}."}

    @staticmethod
    async def mark_unavailable_after_appointment(conn, doctor_id, date, time):
        await DoctorAvailability.update_availability(conn, doctor_id, date, time, is_available=0)
        return {"message": f"Doctor {doctor_id} marked as unavailable for {date} at {time}."}
