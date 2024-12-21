from app.api.employee_routes import employee_bp
from app.api.doctor_routes import doctor_bp
from app.api.nurse_routes import nurse_bp
from app.api.patient_routes import patient_bp

# Blueprint'leri bir liste olarak organize edelim
blueprints = [employee_bp, doctor_bp, nurse_bp, patient_bp]
