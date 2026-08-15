from email_validator import EmailNotValidError, validate_email
from flask import Blueprint, current_app, jsonify, request
from flask_security import hash_password
from app.extensions import db

auth_bp = Blueprint("auth", __name__, url_prefix="/api/auth")


def _get_datastore():
    return current_app.extensions["security"].datastore


@auth_bp.post("/register")
def register():
    data = request.get_json(silent=True) or {}
    name = (data.get("name") or "").strip()
    raw_email = (data.get("email") or "").strip().lower()
    password = data.get("password") or ""

    if not name:
        return jsonify({"error": "Name is required."}), 400
    if len(name) > 120:
        return jsonify({"error": "Name must be 120 characters or fewer."}), 400
    if not raw_email:
        return jsonify({"error": "Email address is required."}), 400

    try:
        valid = validate_email(raw_email, check_deliverability=False)
        email = valid.normalized.lower()
    except EmailNotValidError as exc:
        return jsonify({"error": str(exc)}), 400

    if len(password) < 6:
        return (
            jsonify({"error": "Password must be at least 6 characters long."}),
            400,
        )

    datastore = _get_datastore()
    if datastore.find_user(email=email):
        return (
            jsonify({"error": "An account with this email already exists."}),
            409,
        )

    user = datastore.create_user(
        name=name,
        email=email,
        password=hash_password(password),
        active=True,
    )
    db.session.commit()

    token = user.get_auth_token()
    return (
        jsonify(
            {
                "message": "Account created successfully.",
                "token": token,
                "user": user.to_dict(),
            }
        ),
        201,
    )
