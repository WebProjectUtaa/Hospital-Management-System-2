from app.db.models import Nurse

class NurseService:
    @staticmethod
    async def assign_patient_to_nurse(conn, nurse_id, patient_id):
        """
        Hemşireye bir hasta atar.
        """
        await Nurse.assign_patient(conn, nurse_id, patient_id)
        return {"message": "Patient successfully assigned to nurse."}

    @staticmethod
    async def get_nurse_patients(conn, nurse_id):
        """
        Belirli bir hemşirenin atandığı hastaları döner.
        """
        patients = await Nurse.get_assigned_patients(conn, nurse_id)
        if not patients:
            return {"message": "No patients assigned to this nurse."}
        return patients

    @staticmethod
    async def update_patient_status(conn, patient_id, status):
        """
        Bir hastanın durumunu günceller.
        """
        await Nurse.update_patient_status(conn, patient_id, status)
        return {"message": f"Patient status updated to '{status}'."}

    @staticmethod
    async def get_lab_tests_for_nurse(conn, nurse_id):
        """
        Hemşireye atanan hastaların laboratuvar testlerini döner.
        """
        lab_tests = await Nurse.get_assigned_lab_tests(conn, nurse_id)
        if not lab_tests:
            return {"message": "No lab tests found for patients assigned to this nurse."}
        return lab_tests
