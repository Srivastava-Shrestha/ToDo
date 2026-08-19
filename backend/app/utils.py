from datetime import date

VALID_PRIORITIES = {"low", "medium", "high"}


def parse_due_date(value):
    if value is None or value == "":
        return None, None
    if not isinstance(value, str):
        return None, "Due date must be a string in YYYY-MM-DD format."
    try:
        return date.fromisoformat(value.strip()), None
    except ValueError:
        return None, "Due date must be a valid date in YYYY-MM-DD format."


def validate_todo_payload(data: dict, partial: bool = False):
    if not isinstance(data, dict):
        return None, "Request body must be a JSON object."

    cleaned = {}

    if not partial or "title" in data:
        title = data.get("title")
        if not isinstance(title, str) or not title.strip():
            return None, "Task title is required."
        title = title.strip()
        if len(title) > 200:
            return None, "Task title must be 200 characters or fewer."
        cleaned["title"] = title

    if "description" in data or not partial:
        description = data.get("description", "")
        if description is None:
            description = ""
        if not isinstance(description, str):
            return None, "Description must be a string."
        description = description.strip()
        if len(description) > 2000:
            return None, "Description must be 2000 characters or fewer."
        cleaned["description"] = description

    if "priority" in data or not partial:
        priority = data.get("priority", "medium")
        if not isinstance(priority, str) or priority.strip().lower() not in VALID_PRIORITIES:
            return None, "Priority must be one of: low, medium, high."
        cleaned["priority"] = priority.strip().lower()

    if "due_date" in data or not partial:
        parsed_date, err = parse_due_date(data.get("due_date"))
        if err:
            return None, err
        cleaned["due_date"] = parsed_date

    if "is_completed" in data:
        is_completed = data.get("is_completed")
        if not isinstance(is_completed, bool):
            return None, "is_completed must be a boolean."
        cleaned["is_completed"] = is_completed

    return cleaned, None
