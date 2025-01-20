import sys
from os.path import dirname, abspath
from sanic import Sanic

# Proje root dizinini PYTHONPATH'e ekle
sys.path.append(dirname(dirname(abspath(__file__))))
from app.api.nurse_routes import nurse_bp
from app.db.init_db import init_db, close_db

app = Sanic("NurseService")

# Register blueprints
app.blueprint(nurse_bp)

@app.listener("before_server_start")
async def setup_db(app, loop):
    """Initialize database connection before the server starts."""
    await init_db()

@app.listener("after_server_stop")
async def teardown_db(app, loop):
    """Close database connection after the server stops."""
    await close_db()

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8006, debug=True)
