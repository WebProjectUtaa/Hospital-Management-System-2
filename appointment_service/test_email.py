import asyncio
from app.db.init_db import init_db, get_db_connection
from app.services.appointment_service import AppointmentService

async def test_appointment_workflow():
    await init_db()
    conn = await get_db_connection()

    try:
        # Randevu Oluşturma
        print("Testing Appointment Creation...")
        creation_result = await AppointmentService.create_appointment(
            conn, 
            patient_id=3, 
            doctor_id=3,
            date="2023-12-23", 
            time="10:00:00", 
            reason="Routine Check-up"
        )
        print("Appointment Creation Result:", creation_result)

        # Yeni Oluşturulan Randevunun ID'sini Al
        query = "SELECT MAX(appointment_id) AS latest_appointment_id FROM appointments"
        async with conn.cursor() as cur:
            await cur.execute(query)
            latest_appointment = await cur.fetchone()
            appointment_id = latest_appointment["latest_appointment_id"]
            print("Latest Appointment ID:", appointment_id)

        # Randevuyu İptal Etme
        print("Testing Appointment Cancellation...")
        cancel_result = await AppointmentService.cancel_appointment(conn, appointment_id=appointment_id)
        print("Appointment Cancellation Result:", cancel_result)

    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        if conn:
            await conn.ensure_closed()

if __name__ == "__main__":
    asyncio.run(test_appointment_workflow())
