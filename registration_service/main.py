import sys
from os.path import dirname, abspath
from sanic import Sanic

# Proje root dizinini PYTHONPATH'e ekle
sys.path.append(dirname(dirname(abspath(__file__))))
from app.api.__init__ import patient_bp, employee_bp, record_bp, department_bp
from app.db.init_db import init_db, close_db

app = Sanic("RegistrationService")

app.blueprint(patient_bp)
app.blueprint(employee_bp)
app.blueprint(record_bp)
app.blueprint(department_bp)

@app.before_server_start
async def setup_db(app, loop):
    await init_db()

@app.after_server_stop
async def shutdown_db(app, loop):
    await close_db()

if __name__ == "__main__":
    app.run(host="0.0.0.0", 
            port=8002, 
            debug=True,
            auto_reload=True)
