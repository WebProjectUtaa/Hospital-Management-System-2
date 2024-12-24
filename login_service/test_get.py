import asyncio
from app.db.init_db import init_db, get_db_connection
from app.db.models import LoginModel

async def test_login_model():
    await init_db()
    conn = await get_db_connection()

    try:
        # get_user_by_email test
        print("Testing get_user_by_email...")
        user = await LoginModel.get_user_by_email(conn, email="john.doe@example.com", role="doctor")
        print("get_user_by_email (doctor role) Result:", user)

        user_no_role = await LoginModel.get_user_by_email(conn, email="jane.smith@example.com")
        print("get_user_by_email (no role) Result:", user_no_role)

        invalid_user = await LoginModel.get_user_by_email(conn, email="nonexistent@example.com")
        print("get_user_by_email (invalid email) Result:", invalid_user)

        # get_patient_by_email test
        print("Testing get_patient_by_email...")
        patient = await LoginModel.get_patient_by_email(conn, email="webprojectutaa@gmail.com")
        print("get_patient_by_email Result:", patient)

        invalid_patient = await LoginModel.get_patient_by_email(conn, email="nonexistent@example.com")
        print("get_patient_by_email (invalid email) Result:", invalid_patient)

    finally:
        await conn.ensure_closed()

if __name__ == "__main__":
    asyncio.run(test_login_model())
