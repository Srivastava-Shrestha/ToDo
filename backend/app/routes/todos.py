from datetime import datetime, timezone
from flask import Blueprint, jsonify, request
from flask_security import auth_required, current_user
from app.extensions import db
from app.models import Todo
from app.utils import validate_todo_payload

todos_bp = Blueprint("todos", __name__, url_prefix="/api/todos")


def _get_user_todo(todo_id: int):
    return Todo.query.filter_by(id=todo_id, user_id=current_user.id).first()


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


@todos_bp.get("/<int:todo_id>")
@auth_required("token")
def get_todo(todo_id: int):
    todo = _get_user_todo(todo_id)
    if not todo:
        return jsonify({"error": "Task not found."}), 404
    return jsonify({"todo": todo.to_dict()}), 200


@todos_bp.put("/<int:todo_id>")
@auth_required("token")
def update_todo(todo_id: int):
    todo = _get_user_todo(todo_id)
    if not todo:
        return jsonify({"error": "Task not found."}), 404

    data = request.get_json(silent=True)
    cleaned, err = validate_todo_payload(data, partial=True)
    if err:
        return jsonify({"error": err}), 400

    if "title" in cleaned:
        todo.title = cleaned["title"]
    if "description" in cleaned:
        todo.description = cleaned["description"]
    if "priority" in cleaned:
        todo.priority = cleaned["priority"]
    if "due_date" in cleaned:
        todo.due_date = cleaned["due_date"]
    if "is_completed" in cleaned:
        todo.is_completed = cleaned["is_completed"]
        todo.completed_at = (
            datetime.now(timezone.utc) if cleaned["is_completed"] else None
        )

    db.session.commit()
    return (
        jsonify({"message": "Task updated successfully.", "todo": todo.to_dict()}),
        200,
    )


@todos_bp.patch("/<int:todo_id>/toggle")
@auth_required("token")
def toggle_todo(todo_id: int):
    todo = _get_user_todo(todo_id)
    if not todo:
        return jsonify({"error": "Task not found."}), 404

    todo.is_completed = not todo.is_completed
    todo.completed_at = datetime.now(timezone.utc) if todo.is_completed else None
    db.session.commit()

    return (
        jsonify({"message": "Task status updated.", "todo": todo.to_dict()}),
        200,
    )


@todos_bp.delete("/<int:todo_id>")
@auth_required("token")
def delete_todo(todo_id: int):
    todo = _get_user_todo(todo_id)
    if not todo:
        return jsonify({"error": "Task not found."}), 404

    db.session.delete(todo)
    db.session.commit()
    return jsonify({"message": "Task deleted successfully."}), 200

