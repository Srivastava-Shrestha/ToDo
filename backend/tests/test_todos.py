def test_todos_requires_authentication(client):
    res = client.get("/api/todos")
    assert res.status_code == 401


def test_create_and_list_todos(client, auth_headers):
    create_res = client.post(
        "/api/todos",
        headers=auth_headers,
        json={
            "title": "Submit placement project",
            "description": "Complete README and push commits",
            "priority": "high",
            "due_date": "2026-09-30",
        },
    )
    assert create_res.status_code == 201
    todo = create_res.get_json()["todo"]
    assert todo["title"] == "Submit placement project"
    assert todo["priority"] == "high"
    assert todo["due_date"] == "2026-09-30"
    assert todo["is_completed"] is False

    list_res = client.get("/api/todos", headers=auth_headers)
    assert list_res.status_code == 200
    body = list_res.get_json()
    assert len(body["todos"]) == 1
    assert body["counts"]["total"] == 1
    assert body["counts"]["active"] == 1
    assert body["counts"]["completed"] == 0


def test_create_todo_validation(client, auth_headers):
    missing_title = client.post(
        "/api/todos",
        headers=auth_headers,
        json={"title": "   "},
    )
    assert missing_title.status_code == 400

    bad_priority = client.post(
        "/api/todos",
        headers=auth_headers,
        json={"title": "Valid title", "priority": "urgent"},
    )
    assert bad_priority.status_code == 400

    bad_date = client.post(
        "/api/todos",
        headers=auth_headers,
        json={"title": "Valid title", "due_date": "30-09-2026"},
    )
    assert bad_date.status_code == 400


def test_update_toggle_and_delete_todo(client, auth_headers):
    created = client.post(
        "/api/todos",
        headers=auth_headers,
        json={"title": "Initial task", "priority": "low"},
    ).get_json()["todo"]
    todo_id = created["id"]

    update_res = client.put(
        f"/api/todos/{todo_id}",
        headers=auth_headers,
        json={
            "title": "Updated task title",
            "description": "Added notes",
            "priority": "medium",
        },
    )
    assert update_res.status_code == 200
    updated = update_res.get_json()["todo"]
    assert updated["title"] == "Updated task title"
    assert updated["description"] == "Added notes"
    assert updated["priority"] == "medium"

    toggle_res = client.patch(
        f"/api/todos/{todo_id}/toggle",
        headers=auth_headers,
    )
    assert toggle_res.status_code == 200
    toggled = toggle_res.get_json()["todo"]
    assert toggled["is_completed"] is True
    assert toggled["completed_at"] is not None

    delete_res = client.delete(f"/api/todos/{todo_id}", headers=auth_headers)
    assert delete_res.status_code == 200

    get_deleted = client.get(f"/api/todos/{todo_id}", headers=auth_headers)
    assert get_deleted.status_code == 404


def test_filter_and_clear_completed(client, auth_headers):
    t1 = client.post(
        "/api/todos",
        headers=auth_headers,
        json={"title": "Write API docs", "priority": "high"},
    ).get_json()["todo"]
    client.post(
        "/api/todos",
        headers=auth_headers,
        json={"title": "Buy groceries", "priority": "low"},
    )

    client.patch(f"/api/todos/{t1['id']}/toggle", headers=auth_headers)

    active_res = client.get("/api/todos?status=active", headers=auth_headers)
    assert len(active_res.get_json()["todos"]) == 1
    assert active_res.get_json()["todos"][0]["title"] == "Buy groceries"

    completed_res = client.get("/api/todos?status=completed", headers=auth_headers)
    assert len(completed_res.get_json()["todos"]) == 1
    assert completed_res.get_json()["todos"][0]["title"] == "Write API docs"

    search_res = client.get("/api/todos?search=groceries", headers=auth_headers)
    assert len(search_res.get_json()["todos"]) == 1

    clear_res = client.delete("/api/todos/completed", headers=auth_headers)
    assert clear_res.status_code == 200
    assert clear_res.get_json()["deleted_count"] == 1

    remaining = client.get("/api/todos", headers=auth_headers).get_json()
    assert remaining["counts"]["total"] == 1
    assert remaining["counts"]["completed"] == 0


def test_user_isolation(client, auth_headers):
    todo = client.post(
        "/api/todos",
        headers=auth_headers,
        json={"title": "Private user 1 task"},
    ).get_json()["todo"]

    user2_res = client.post(
        "/api/auth/register",
        json={
            "name": "Second User",
            "email": "second@example.com",
            "password": "Password123!",
        },
    )
    user2_headers = {"Authentication-Token": user2_res.get_json()["token"]}

    list_user2 = client.get("/api/todos", headers=user2_headers).get_json()
    assert len(list_user2["todos"]) == 0

    forbidden_get = client.get(f"/api/todos/{todo['id']}", headers=user2_headers)
    assert forbidden_get.status_code == 404
