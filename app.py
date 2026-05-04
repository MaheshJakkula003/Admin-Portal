from flask import Flask, jsonify
from config import Config
from models import db, Admin
from flask_login import LoginManager
from flask_cors import CORS

app = Flask(
    __name__,
    template_folder="templates",
    static_folder="static"
)

app.config.from_object(Config)

CORS(
    app,
    supports_credentials=True,
    origins=["http://127.0.0.1:5000", "http://localhost:5000"]
)

db.init_app(app)

login_manager = LoginManager()
login_manager.init_app(app)

login_manager.login_view = None
login_manager.login_message = None

app.config.update(
    SESSION_COOKIE_HTTPONLY=True,
    SESSION_COOKIE_SAMESITE="Lax",
    SESSION_COOKIE_SECURE=False
)

@login_manager.user_loader
def load_user(user_id):
    try:
        return db.session.get(Admin, int(user_id))
    except:
        return None

@login_manager.unauthorized_handler
def unauthorized():
    return jsonify({"error": "Unauthorized. Please login."}), 401

import routes
app.register_blueprint(routes.routes)

@app.route("/test")
def test():
    return {"status": "App running successfully"}

def create_db():
    with app.app_context():
        db.create_all()
        print("Database created successfully")

if __name__ == "__main__":
    create_db()

    app.run(
        host="127.0.0.1",
        port=5000,
        debug=True
    )