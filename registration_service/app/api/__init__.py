from app.api.patient_routes import patient_bp
from app.api.employee_routes import employee_bp
from app.api.patient_record_routes import record_bp
from app.api.department_routes import department_bp

blueprints = [patient_bp, employee_bp, record_bp, department_bp]
