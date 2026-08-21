from datetime import datetime, timezone
from flask import Blueprint, jsonify, request
from flask_security import auth_required, current_user
from app.extensions import db
from app.models import Todo
from app.utils import validate_todo_payload

todos_bp = Blueprint("todos", __name__, url_prefix="/api/todos")


@todos_bp.get("")
@auth_required("token")
def list_todos():
    todos = (
        Todo.query.filter_by(user_id=current_user.id)
        .order_by(Todo.is_completed.asc(), Todo.created_at.desc())
        .all()
    )
    return jsonify({"todos": [todo.to_dict() for todo in todos]}), 200


@todos_bp.post("")
@auth_required("token")
def create_todo():
    data = request.get_json(silent=True)
    cleaned, err = validate_todo_payload(data, partial=False)
    if err:
        return jsonify({"error": err}), 400

    is_completed = cleaned.get("is_completed", False)
    todo = Todo(
        user_id=current_user.id,
        title=cleaned["title"],
        description=cleaned["description"],
        priority=cleaned["priority"],
        due_date=cleaned["due_date"],
        is_completed=is_completed,
        completed_at=datetime.now(timezone.utc) if is_completed else None,
    )
    db.session.add(todo)
    db.session.commit()

    return (
        jsonify({"message": "Task created successfully.", "todo": todo.to_dict()}),
        201,
    )
