from app.db.models import Department

class DepartmentService:
    @staticmethod
    async def add_department(conn, department_id, department_name, employee_id):
        """
        Yeni bir bölüm ekler.
        """
        await Department.add(conn, department_id, department_name, employee_id)
        return {"message": f"Department '{department_name}' added successfully!", "department_id": department_id}

    @staticmethod
    async def update_department(conn, department_id, updates):
        """
        Mevcut bir bölüm bilgilerini günceller.
        """
        update_fields = ", ".join([f"{key} = %s" for key in updates.keys()])
        query = f"""
        UPDATE departments
        SET {update_fields}
        WHERE department_id = %s
        """
        async with conn.cursor() as cur:
            await cur.execute(query, (*updates.values(), department_id))
            await conn.commit()
        return {"message": f"Department with ID {department_id} updated successfully!"}

    @staticmethod
    async def delete_department(conn, department_id):
        """
        Bir bölümü siler.
        """
        query = "DELETE FROM departments WHERE department_id = %s"
        async with conn.cursor() as cur:
            await cur.execute(query, (department_id,))
            await conn.commit()
        return {"message": f"Department with ID {department_id} deleted successfully!"}

    @staticmethod
    async def get_all_departments(conn):
        """
        Tüm bölümleri listeler.
        """
        departments = await Department.get_all(conn)
        return departments
