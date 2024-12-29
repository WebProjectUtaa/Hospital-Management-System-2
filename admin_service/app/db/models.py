class AdminModel:
    @staticmethod
    async def get_all_users(conn):
        """
        Tüm kullanıcıları döndürür.
        """
        query = """
        SELECT id, Employee_name, surname, role, email, gender, department
        FROM employees
        """
        async with conn.cursor() as cur:
            await cur.execute(query)
            return await cur.fetchall()

    @staticmethod
    async def get_users_by_role(conn, role):
        """
        Belirli bir role sahip kullanıcıları döndürür.
        """
        query = """
        SELECT id, Employee_name, surname, email, gender, department
        FROM employees
        WHERE role = %s
        """
        async with conn.cursor() as cur:
            await cur.execute(query, (role,))
            return await cur.fetchall()

    @staticmethod
    async def add_user(conn, name, surname, role, email, gender, department, password):
        """
        Yeni bir kullanıcı ekler.
        """
        query = """
        INSERT INTO employees (Employee_name, surname, role, email, gender, department, Employee_password)
        VALUES (%s, %s, %s, %s, %s, %s, %s)
        """
        await conn.execute(query, (name, surname, role, email, gender, department, password))

    @staticmethod
    async def update_user(conn, user_id, updates):
        """
        Mevcut bir kullanıcıyı günceller.
        """
        fields = ", ".join([f"{key} = %s" for key in updates.keys()])
        values = list(updates.values()) + [user_id]
        query = f"""
        UPDATE employees
        SET {fields}
        WHERE id = %s
        """
        await conn.execute(query, values)

    @staticmethod
    async def delete_user(conn, user_id):
        """
        Kullanıcıyı siler.
        """
        query = """
        DELETE FROM employees
        WHERE id = %s
        """
        await conn.execute(query, (user_id,))

    @staticmethod
    async def get_departments(conn):
        """
        Tüm departmanları döndürür.
        """
        query = """
        SELECT department_id, department_name
        FROM departments
        """
        async with conn.cursor() as cur:
            await cur.execute(query)
            return await cur.fetchall()

    @staticmethod
    async def add_department(conn, department_name):
        """
        Yeni bir departman ekler.
        """
        query = """
        INSERT INTO departments (department_name)
        VALUES (%s)
        """
        await conn.execute(query, (department_name,))

    @staticmethod
    async def update_department(conn, department_id, department_name):
        """
        Mevcut bir departmanı günceller.
        """
        query = """
        UPDATE departments
        SET department_name = %s
        WHERE department_id = %s
        """
        await conn.execute(query, (department_name, department_id))

    @staticmethod
    async def delete_department(conn, department_id):
        """
        Departmanı siler.
        """
        query = """
        DELETE FROM departments
        WHERE department_id = %s
        """
        await conn.execute(query, (department_id,))
