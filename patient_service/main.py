from sanic import Sanic
from app.api.patient_routes import patient_bp
from app.db.init_db import init_db, close_db

app = Sanic("PatientService")

# Register blueprints
app.blueprint(patient_bp)

@app.listener("before_server_start")
async def setup_db(app, loop):
    """Initialize database connection before the server starts."""
    await init_db()

@app.listener("after_server_stop")
async def teardown_db(app, loop):
    """Close database connection after the server stops."""
    await close_db()

if __name__ == "__main__":
    app.run(host="localhost", port=8007, debug=True)
