from app.db.models import PatientModel

class PatientService:
    @staticmethod
    async def get_patient_details(conn, patient_id):
        """
        Hastanın detaylarını getir.
        """
        patient = await PatientModel.get_patient_by_id(conn, patient_id)
        if not patient:
            raise ValueError(f"Patient with ID {patient_id} not found.")
        return patient

    @staticmethod
    async def get_medical_history(conn, patient_id):
        """
        Hastanın tıbbi geçmişini getir.
        """
        history = await PatientModel.get_medical_history(conn, patient_id)
        return history

    @staticmethod
    async def get_lab_tests(conn, patient_id):
        """
        Hastanın laboratuvar testlerini getir.
        """
        lab_tests = await PatientModel.get_lab_tests(conn, patient_id)
        return lab_tests

    @staticmethod
    async def get_prescriptions(conn, patient_id):
        """
        Hastanın reçetelerini getir.
        """
        prescriptions = await PatientModel.get_prescriptions(conn, patient_id)
        return prescriptions
