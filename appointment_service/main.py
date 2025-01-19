import sys
from os.path import dirname, abspath
sys.path.append(dirname(dirname(abspath(__file__))))

from sanic import Sanic
from app.api.appointment_routes import appointment_bp
from app.db.init_db import init_db, close_db

app = Sanic("AppointmentService")

app.blueprint(appointment_bp)

@app.listener("before_server_start")
async def setup_db(app, loop):
    await init_db()

@app.listener("after_server_stop")
async def teardown_db(app, loop):
    await close_db()

if __name__ == "__main__":
    app.run(host = "localhost", port = 8003, debug = True)
    
