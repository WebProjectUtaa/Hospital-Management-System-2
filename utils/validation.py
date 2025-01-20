def validate_appointment_data(data):
    required_fields = ["patient_id", "doctor_id", "appointment_date", "appointment_time", "reason"]
    missing_fields = [field for field in required_fields if field not in data]
    if missing_fields:
        raise ValueError(f"Missing fields: {', '.join(missing_fields)}")
