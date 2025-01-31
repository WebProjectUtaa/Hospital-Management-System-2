import sys
from os.path import dirname, abspath
from sanic import Sanic

# Proje root dizinini PYTHONPATH'e ekle
sys.path.append(dirname(dirname(abspath(__file__))))
from login_service.app.api.login_routes import login_bp
from login_service.app.db.init_db import init_db, close_db


app = Sanic("LoginService")

# Register blueprints
app.blueprint(login_bp)

@app.listener("before_server_start")
async def setup_db(app, loop):
    """Initialize database connection before the server starts."""
    await init_db()

@app.listener("after_server_stop")
async def teardown_db(app, loop):
    """Close database connection after the server stops."""
    await close_db()

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8001, debug=True, access_log=True)
