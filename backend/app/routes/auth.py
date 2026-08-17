import uuid
from email_validator import EmailNotValidError, validate_email
from flask import Blueprint, current_app, jsonify, request
from flask_security import auth_required, current_user, hash_password, verify_password
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


@auth_bp.post("/login")
def login():
    data = request.get_json(silent=True) or {}
    email = (data.get("email") or "").strip().lower()
    password = data.get("password") or ""

    if not email or not password:
        return jsonify({"error": "Email and password are required."}), 400

    datastore = _get_datastore()
    user = datastore.find_user(email=email)

    if not user or not user.active or not verify_password(password, user.password):
        return jsonify({"error": "Invalid email or password."}), 401

    token = user.get_auth_token()
    return (
        jsonify(
            {
                "message": "Logged in successfully.",
                "token": token,
                "user": user.to_dict(),
            }
        ),
        200,
    )


@auth_bp.post("/logout")
@auth_required("token")
def logout():
    current_user.fs_uniquifier = uuid.uuid4().hex
    db.session.commit()
    return jsonify({"message": "Logged out successfully."}), 200


@auth_bp.get("/me")
@auth_required("token")
def get_current_user():
    return jsonify({"user": current_user.to_dict()}), 200

