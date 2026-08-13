from pathlib import Path
from flask import Flask, jsonify
from flask_security import SQLAlchemyUserDatastore
from app.config import BASE_DIR, CONFIG_MAP
from app.extensions import cors, db, security
from app.models import Role, User

user_datastore = SQLAlchemyUserDatastore(db, User, Role)


def create_app(config_name: str = "default") -> Flask:
    app = Flask(__name__)
    config_cls = CONFIG_MAP.get(config_name, CONFIG_MAP["default"])
    app.config.from_object(config_cls)

    instance_dir = Path(BASE_DIR) / "instance"
    instance_dir.mkdir(parents=True, exist_ok=True)

    db.init_app(app)
    security.init_app(app, user_datastore, register_blueprint=False)
    cors.init_app(
        app,
        resources={r"/api/*": {"origins": app.config["CORS_ORIGINS"]}},
        expose_headers=["Authentication-Token"],
        allow_headers=["Content-Type", "Authentication-Token", "Authorization"],
    )

    @app.get("/api/health")
    def health_check():
        return jsonify({"status": "ok", "service": "todo-api"}), 200

    with app.app_context():
        db.create_all()

    return app

