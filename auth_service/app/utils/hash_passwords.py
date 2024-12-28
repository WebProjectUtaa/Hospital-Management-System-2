import os
import bcrypt
import asyncio
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))
from app.db.init_db import get_db_connection, init_db

async def hash_existing_passwords():
    await init_db()
    async with await get_db_connection() as conn:
        async with conn.cursor() as cur:
            print("Hashing passwords for employees...")

            # Employees table: Fetch only valid rows
            await cur.execute("SELECT id, Employee_password FROM employees WHERE Employee_password IS NOT NULL")
            employees = await cur.fetchall()

            for employee in employees:
                try:
                    # Access dictionary keys directly
                    id = employee['id']
                    password = employee['Employee_password']

                    # Skip if the password is already hashed
                    if password.startswith("$2b$"):
                        print(f"Skipping employee ID {id}, already hashed.")
                        continue

                    # Hash the password and update the database
                    hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
                    await cur.execute(
                        "UPDATE employees SET Employee_password = %s WHERE id = %s", 
                        (hashed_password, id)
                    )
                    print(f"Hashed password for employee ID {id}.")
                except Exception as e:
                    print(f"Error processing employee ID {employee}: {e}")

            print("Hashing passwords for patients...")

            # Patients table: Fetch only valid rows
            await cur.execute("SELECT patient_id, password FROM patients WHERE password IS NOT NULL")
            patients = await cur.fetchall()

            for patient in patients:
                try:
                    # Access dictionary keys directly
                    id = patient['patient_id']
                    password = patient['password']

                    # Skip if the password is already hashed
                    if password.startswith("$2b$"):
                        print(f"Skipping patient ID {id}, already hashed.")
                        continue

                    # Hash the password and update the database
                    hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
                    await cur.execute(
                        "UPDATE patients SET password = %s WHERE patient_id = %s", 
                        (hashed_password, id)
                    )
                    print(f"Hashed password for patient ID {id}.")
                except Exception as e:
                    print(f"Error processing patient ID {patient}: {e}")

            # Commit changes to the database
            await conn.commit()
            print("Passwords have been hashed successfully!")

if __name__ == "__main__":
    asyncio.run(hash_existing_passwords())
