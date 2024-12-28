from sanic import Sanic
from app.api.auth_routes import auth_bp
from app.db.init_db import init_db, close_db

app = Sanic("AuthService")

# Blueprint'i kaydet
app.blueprint(auth_bp)

@app.before_server_start
async def setup_db(app, loop):
    await init_db()

@app.after_server_stop
async def shutdown_db(app, loop):
    await close_db()

if __name__ == "__main__":
    app.run(host="localhost", port=8000, debug=True)
