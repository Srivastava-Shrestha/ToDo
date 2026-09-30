# ToDo — Minimalist Task Management Application

## 1. Project Overview

**ToDo** is a clean, full-stack task management web application designed for focused personal productivity. It provides a lightweight RESTful API backend built with **Flask**, **SQLAlchemy**, and **Flask-Security** alongside a responsive **Vue 3** single-page frontend powered by **Vite** and **Axios**.

Every user has an isolated workspace protected by token-based authentication, with support for task priorities, due dates, overdue detection, inline editing, and instant filtering.

---

## 2. Features

- **User Authentication**:
  - Account registration and login with server-side validation and `bcrypt` password hashing.
  - Token-based authentication via `Flask-Security` (`Authentication-Token` header).
  - Instant token revocation on sign-out via `fs_uniquifier` rotation.
- **Complete Task CRUD**:
  - Create tasks with a title, optional notes/description, priority (`low`, `medium`, `high`), and due date.
  - Read and list user-scoped tasks with real-time counts (`total`, `active`, `completed`, `overdue`).
  - Update task details inline or toggle completion status with a single click.
  - Delete individual tasks or bulk-clear all completed tasks at once.
- **Filtering, Search & Smart Ordering**:
  - Filter tasks by status (`all`, `active`, `completed`) and priority (`low`, `medium`, `high`).
  - Case-insensitive keyword search across task titles and descriptions.
  - Automatic ordering that keeps incomplete, due-soon, and higher-priority tasks at the top.
- **Minimalist & Responsive UI**:
  - Distraction-free interface with keyboard shortcuts (`N` to focus new task input, `/` to focus search, `Esc` to cancel inline editing).

---

## 3. Tech Stack

| Layer | Technologies |
| :--- | :--- |
| **Backend** | Python 3, Flask, Flask-SQLAlchemy, Flask-Security-Too, Flask-CORS, SQLite |
| **Frontend** | Vue 3 (Composition API), Vue Router 4, Axios, Vite, Custom CSS |
| **Testing** | Pytest |

---

## 4. Project Structure

```text
ToDo/
├── backend/
│   ├── app/
│   │   ├── models/
│   │   │   ├── __init__.py
│   │   │   ├── user.py          # User and Role models (Flask-Security)
│   │   │   └── todo.py          # Todo model with priority & due date
│   │   ├── routes/
│   │   │   ├── __init__.py
│   │   │   ├── auth.py          # Registration, login, logout, profile
│   │   │   └── todos.py         # RESTful CRUD & filtering endpoints
│   │   ├── __init__.py          # Flask application factory & error handlers
│   │   ├── config.py            # Environment & security configurations
│   │   ├── extensions.py        # SQLAlchemy, Security, CORS instances
│   │   └── utils.py             # Payload validation utilities
│   ├── tests/
│   │   ├── conftest.py          # Pytest fixtures
│   │   ├── test_auth.py         # Authentication test suite
│   │   └── test_todos.py        # Todo CRUD & user isolation tests
│   ├── .env.example
│   ├── requirements.txt
│   └── run.py                   # Entry point
├── frontend/
│   ├── src/
│   │   ├── assets/
│   │   │   └── styles.css       # Design tokens & minimalist stylesheet
│   │   ├── components/
│   │   │   ├── Navbar.vue
│   │   │   ├── TodoFilterBar.vue
│   │   │   ├── TodoForm.vue
│   │   │   └── TodoItem.vue
│   │   ├── router/
│   │   │   └── index.js         # Protected & guest route guards
│   │   ├── services/
│   │   │   └── api.js           # Axios instance & token interceptors
│   │   ├── store/
│   │   │   └── auth.js          # Reactive authentication store
│   │   ├── views/
│   │   │   ├── LoginView.vue
│   │   │   ├── RegisterView.vue
│   │   │   └── TodoView.vue
│   │   ├── App.vue
│   │   └── main.js
│   ├── index.html
│   ├── package.json
│   └── vite.config.js
└── README.md
```

---

## 5. Installation & Setup Steps

### Prerequisites
- **Python** 3.10+
- **Node.js** 18+ and **npm**

### Step 1: Clone the Repository
```bash
git clone https://github.com/Srivastava-Shrestha/ToDo.git
cd ToDo
```

### Step 2: Backend Setup
```bash
cd backend
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
```

Start the Flask API server (runs on `http://127.0.0.1:5000`):
```bash
python run.py
```

Run the backend test suite:
```bash
pytest -v
```

### Step 3: Frontend Setup
Open a new terminal window:
```bash
cd frontend
npm install
cp .env.example .env
```

Start the Vite development server (runs on `http://localhost:5173`):
```bash
npm run dev
```

Build for production:
```bash
npm run build
```

---

## 6. REST API Documentation

All protected endpoints require the `Authentication-Token` HTTP header returned during login or registration:

```http
Authentication-Token: <token>
Content-Type: application/json
```

### Authentication Endpoints

#### `POST /api/auth/register`
Registers a new user account and returns an authentication token.
- **Request Body**:
  ```json
  {
    "name": "Shrestha Srivastava",
    "email": "shrestha@example.com",
    "password": "securepassword"
  }
  ```
- **Response (`201 Created`)**:
  ```json
  {
    "message": "Account created successfully.",
    "token": "<auth-token>",
    "user": {
      "id": 1,
      "name": "Shrestha Srivastava",
      "email": "shrestha@example.com",
      "created_at": "2026-09-30T12:00:00+00:00"
    }
  }
  ```

#### `POST /api/auth/login`
Authenticates an existing user and issues a fresh authentication token.
- **Request Body**:
  ```json
  {
    "email": "shrestha@example.com",
    "password": "securepassword"
  }
  ```
- **Response (`200 OK`)**:
  ```json
  {
    "message": "Logged in successfully.",
    "token": "<auth-token>",
    "user": {
      "id": 1,
      "name": "Shrestha Srivastava",
      "email": "shrestha@example.com",
      "created_at": "2026-09-30T12:00:00+00:00"
    }
  }
  ```

#### `GET /api/auth/me`
Returns the profile of the currently authenticated user.
- **Headers**: `Authentication-Token: <token>`
- **Response (`200 OK`)**:
  ```json
  {
    "user": {
      "id": 1,
      "name": "Shrestha Srivastava",
      "email": "shrestha@example.com",
      "created_at": "2026-09-30T12:00:00+00:00"
    }
  }
  ```

#### `POST /api/auth/logout`
Invalidates the active authentication token by rotating the user's `fs_uniquifier`.
- **Headers**: `Authentication-Token: <token>`
- **Response (`200 OK`)**:
  ```json
  {
    "message": "Logged out successfully."
  }
  ```

---

### Todo CRUD Endpoints

#### `GET /api/todos`
Lists tasks belonging to the authenticated user along with summary counts.
- **Query Parameters (Optional)**:
  - `status`: `all` (default), `active`, or `completed`
  - `priority`: `low`, `medium`, or `high`
  - `search`: keyword to match against title or description
- **Response (`200 OK`)**:
  ```json
  {
    "todos": [
      {
        "id": 1,
        "user_id": 1,
        "title": "Complete API documentation",
        "description": "Include request and response payloads",
        "priority": "high",
        "due_date": "2026-09-30",
        "is_completed": false,
        "is_overdue": false,
        "completed_at": null,
        "created_at": "2026-09-29T10:15:00+00:00",
        "updated_at": "2026-09-29T10:15:00+00:00"
      }
    ],
    "counts": {
      "total": 1,
      "active": 1,
      "completed": 0,
      "overdue": 0
    }
  }
  ```

#### `POST /api/todos`
Creates a new task for the authenticated user.
- **Request Body**:
  ```json
  {
    "title": "Complete API documentation",
    "description": "Include request and response payloads",
    "priority": "high",
    "due_date": "2026-09-30"
  }
  ```
- **Response (`201 Created`)**:
  ```json
  {
    "message": "Task created successfully.",
    "todo": {
      "id": 1,
      "user_id": 1,
      "title": "Complete API documentation",
      "description": "Include request and response payloads",
      "priority": "high",
      "due_date": "2026-09-30",
      "is_completed": false,
      "is_overdue": false,
      "completed_at": null,
      "created_at": "2026-09-29T10:15:00+00:00",
      "updated_at": "2026-09-29T10:15:00+00:00"
    }
  }
  ```

#### `GET /api/todos/<id>`
Retrieves a single task by ID (must belong to the authenticated user).
- **Response (`200 OK`)**: Returns `{"todo": { ... }}`
- **Error (`404 Not Found`)**: `{"error": "Task not found."}`

#### `PUT /api/todos/<id>`
Updates one or more fields of an existing task (`title`, `description`, `priority`, `due_date`, `is_completed`).
- **Request Body**:
  ```json
  {
    "title": "Finalize API documentation",
    "priority": "medium",
    "due_date": "2026-10-01"
  }
  ```
- **Response (`200 OK`)**: Returns `{"message": "Task updated successfully.", "todo": { ... }}`

#### `PATCH /api/todos/<id>/toggle`
Toggles the `is_completed` state of a task and updates `completed_at`.
- **Response (`200 OK`)**: Returns `{"message": "Task status updated.", "todo": { ... }}`

#### `DELETE /api/todos/<id>`
Deletes a specific task belonging to the authenticated user.
- **Response (`200 OK`)**:
  ```json
  {
    "message": "Task deleted successfully."
  }
  ```

#### `DELETE /api/todos/completed`
Deletes all completed tasks belonging to the authenticated user.
- **Response (`200 OK`)**:
  ```json
  {
    "message": "Cleared 3 completed task(s).",
    "deleted_count": 3
  }
  ```

