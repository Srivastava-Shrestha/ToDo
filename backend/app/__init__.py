from pathlib import Path
from flask import Flask, jsonify
from flask_security import SQLAlchemyUserDatastore
from app.config import BASE_DIR, CONFIG_MAP
from app.extensions import cors, db, security
from app.models import Role, User
from app.routes import auth_bp, todos_bp

user_datastore = SQLAlchemyUserDatastore(db, User, Role)


def create_app(config_name: str = "default") -> Flask:
    app = Flask(__name__)
    config_cls = CONFIG_MAP.get(config_name, CONFIG_MAP["default"])
    app.config.from_object(config_cls)

    instance_dir = Path(BASE_DIR) / "instance"
    instance_dir.mkdir(parents=True, exist_ok=True)

    db.init_app(app)
    security.init_app(app, user_datastore, register_blueprint=False)

    @security.unauthn_handler
    def handle_unauthenticated(mechanisms, headers=None):
        return (
            jsonify({"error": "Authentication token is missing or invalid."}),
            401,
            headers or {},
        )

    @security.unauthz_handler
    def handle_unauthorized(func_name, params):
        return (
            jsonify({"error": "You do not have permission to perform this action."}),
            403,
        )

    cors.init_app(
        app,
        resources={r"/api/*": {"origins": app.config["CORS_ORIGINS"]}},
        expose_headers=["Authentication-Token"],
        allow_headers=["Content-Type", "Authentication-Token", "Authorization"],
    )

    app.register_blueprint(auth_bp)
    app.register_blueprint(todos_bp)

    @app.get("/api/health")
    def health_check():
        return jsonify({"status": "ok", "service": "todo-api"}), 200

    @app.errorhandler(404)
    def not_found_error(_error):
        return jsonify({"error": "Requested resource was not found."}), 404

    @app.errorhandler(405)
    def method_not_allowed_error(_error):
        return jsonify({"error": "Method not allowed for this endpoint."}), 405

    @app.errorhandler(500)
    def internal_server_error(_error):
        db.session.rollback()
        return jsonify({"error": "An internal server error occurred."}), 500

    with app.app_context():
        db.create_all()

    return app

