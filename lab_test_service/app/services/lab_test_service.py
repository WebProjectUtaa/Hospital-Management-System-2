from app.db.models import LabTest

class LabTestService:
    @staticmethod
    async def create_lab_test(conn, patient_id, doctor_id, test_name, priority, test_reason=None):
        """
        Yeni bir laboratuvar testi oluşturur.
        """
        await LabTest.add(conn, patient_id, doctor_id, test_name, priority, test_reason)
        return {"message": "Lab test created successfully."}

    @staticmethod
    async def get_lab_tests_by_doctor(conn, doctor_id):
        """
        Belirli bir doktorun talep ettiği tüm testleri döner.
        """
        tests = await LabTest.get_by_doctor(conn, doctor_id)
        if not tests:
            raise ValueError(f"No lab tests found for doctor ID {doctor_id}.")
        return tests

    @staticmethod
    async def get_lab_tests_by_patient(conn, patient_id):
        """
        Belirli bir hastanın testlerini döner.
        """
        tests = await LabTest.get_by_patient(conn, patient_id)
        if not tests:
            raise ValueError(f"No lab tests found for patient ID {patient_id}.")
        return tests

    @staticmethod
    async def assign_lab_test_to_staff(conn, test_id, staff_id):
        """
        Bir laboratuvar testini laboratuvar personeline atar.
        """
        await LabTest.assign_staff(conn, test_id, staff_id)
        return {"message": "Lab test assigned to staff successfully."}

    @staticmethod
    async def update_lab_test_status(conn, test_id, status, result=None):
        """
        Laboratuvar testinin durumunu günceller.
        """
        await LabTest.update_status(conn, test_id, status, result)
        return {"message": f"Lab test status updated to '{status}'."}

    @staticmethod
    async def delete_lab_test(conn, test_id):
        """
        Laboratuvar testini siler.
        """
        await LabTest.delete(conn, test_id)
        return {"message": f"Lab test with ID {test_id} deleted successfully."}

    @staticmethod
    async def get_patient_email_by_test(conn, test_id):
        """
        Test ID'ye göre hastanın e-posta adresini alır.
        """
        return await LabTest.get_patient_email_by_test(conn, test_id)

    @staticmethod
    async def get_doctor_email_by_test(conn, test_id):
        """
        Test ID'ye göre doktorun e-posta adresini alır.
        """
        return await LabTest.get_doctor_email_by_test(conn, test_id)
