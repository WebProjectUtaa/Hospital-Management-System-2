from app.api.patient_routes import patient_bp
from .patient_record_routes import record_bp

blueprints = [patient_bp, record_bp]
