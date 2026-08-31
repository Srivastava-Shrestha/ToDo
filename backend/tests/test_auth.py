def test_register_success(client):
    res = client.post(
        "/api/auth/register",
        json={
            "name": "Test User",
            "email": "user@example.com",
            "password": "securepassword",
        },
    )
    assert res.status_code == 201
    data = res.get_json()
    assert "token" in data
    assert data["user"]["email"] == "user@example.com"
    assert data["user"]["name"] == "Test User"


def test_register_duplicate_email(client):
    payload = {
        "name": "Test User",
        "email": "duplicate@example.com",
        "password": "securepassword",
    }
    first = client.post("/api/auth/register", json=payload)
    assert first.status_code == 201

    second = client.post("/api/auth/register", json=payload)
    assert second.status_code == 409
    assert "already exists" in second.get_json()["error"]


def test_register_validation_errors(client):
    res_missing_name = client.post(
        "/api/auth/register",
        json={"name": "", "email": "a@example.com", "password": "securepassword"},
    )
    assert res_missing_name.status_code == 400

    res_bad_email = client.post(
        "/api/auth/register",
        json={"name": "User", "email": "not-an-email", "password": "securepassword"},
    )
    assert res_bad_email.status_code == 400

    res_short_pw = client.post(
        "/api/auth/register",
        json={"name": "User", "email": "a@example.com", "password": "123"},
    )
    assert res_short_pw.status_code == 400


def test_login_and_current_user(client):
    client.post(
        "/api/auth/register",
        json={
            "name": "Login User",
            "email": "login@example.com",
            "password": "mypassword123",
        },
    )

    login_res = client.post(
        "/api/auth/login",
        json={"email": "login@example.com", "password": "mypassword123"},
    )
    assert login_res.status_code == 200
    token = login_res.get_json()["token"]

    me_res = client.get(
        "/api/auth/me",
        headers={"Authentication-Token": token},
    )
    assert me_res.status_code == 200
    assert me_res.get_json()["user"]["email"] == "login@example.com"


def test_login_invalid_credentials(client):
    res = client.post(
        "/api/auth/login",
        json={"email": "nonexistent@example.com", "password": "wrongpassword"},
    )
    assert res.status_code == 401


def test_logout_invalidates_token(client, auth_headers):
    logout_res = client.post("/api/auth/logout", headers=auth_headers)
    assert logout_res.status_code == 200

    me_after = client.get("/api/auth/me", headers=auth_headers)
    assert me_after.status_code == 401
