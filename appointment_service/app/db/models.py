from aiomysql import DictCursor

class Branch:
    table_name = "branches"

    @staticmethod
    async def get_all(conn):
        query = "SELECT branch_id, branch_name FROM branches"
        async with conn.cursor(DictCursor) as cur:
            await cur.execute(query)
            return await cur.fetchall()


class DoctorAvailability:
    table_name = "doctor_availability"

    @staticmethod
    async def get_available_doctors(conn, branch_id, date, time):
        query = """
        SELECT d.id, e.Employee_name, e.surname, da.available_date, da.available_time 
        FROM doctor_availability da
        INNER JOIN doctors d ON da.doctor_id = d.id
        INNER JOIN employees e ON d.id = e.id
        WHERE d.branch_id = %s AND da.available_date = %s AND da.available_time = %s AND da.is_available = 1
        """
        async with conn.cursor(DictCursor) as cur:
            await cur.execute(query, (branch_id, date, time))
            return await cur.fetchall()

    @staticmethod
    async def update_availability(conn, doctor_id, date, time, is_available):
        query = """
        UPDATE doctor_availability 
        SET is_available = %s 
        WHERE doctor_id = %s AND available_date = %s AND available_time = %s
        """
        async with conn.cursor() as cur:
            await cur.execute(query, (is_available, doctor_id, date, time))
            await conn.commit()


class Appointment:
    table_name = "appointments"

    @staticmethod
    async def add(conn, patient_id, doctor_id, date, time, reason):
        query = """
        INSERT INTO appointments (patient_id, doctor_id, appointment_date, appointment_time, reason) 
        VALUES (%s, %s, %s, %s, %s)
        """
        async with conn.cursor() as cur:
            await cur.execute(query, (patient_id, doctor_id, date, time, reason))
            await conn.commit()

    @staticmethod
    async def get_by_patient(conn, patient_id):
        query = """
        SELECT appointment_id, doctor_id, appointment_date, appointment_time, reason, status 
        FROM appointments 
        WHERE patient_id = %s
        """
        async with conn.cursor(DictCursor) as cur:
            await cur.execute(query, (patient_id,))
            return await cur.fetchall()

    @staticmethod
    async def update_status(conn, appointment_id, status):
        query = "UPDATE appointments SET status = %s WHERE appointment_id = %s"
        async with conn.cursor() as cur:
            await cur.execute(query, (status, appointment_id))
            await conn.commit()
