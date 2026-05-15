# task-manager-api

> 📌 **Portfolio project** — built as a demonstration for recruiters and technical reviewers.
> Live demo available, see [Live Demo](#live-demo) below.

REST API for personal task management built with Django REST Framework.
Users can organize work into Projects and Tasks with status tracking,
completion percentages and ownership-based access control.

---

## Live Demo

**Base URL:** `https://web-production-dda72.up.railway.app`

> ⚠️ The demo database may be reset periodically.

### Try it in the browser — Browsable API

1. Open [/api-auth/login/](https://web-production-dda72.up.railway.app/api-auth/login/)
2. Log in with the demo credentials below
3. Navigate to any endpoint and interact directly from the browser

| Field | Value |
|-------|-------|
| Username | `test` |
| Password | `password123` |

### Try it with Postman

**Environment setup**

| Variable | Value |
|----------|-------|
| `base_url` | `https://web-production-dda72.up.railway.app` |
| `access_token` | *(fill after login)* |
| `refresh_token` | *(fill after login)* |

**Authentication**

Set `base_url`, then send `POST /api/auth/login/` with the demo credentials.
Copy the tokens from the response into `access_token` and `refresh_token`.
All requests use `Bearer {{access_token}}` via the collection Authorization tab.

> 💡 You can use a Postman post-response script to automate token saving.

---

## Tech Stack
- Python 3.12
- Django 6.0
- Django REST Framework
- JWT Authentication (djangorestframework-simplejwt)
- PostgreSQL (production) / SQLite (development)
- Docker + Nginx (local development)
- Deployed on Railway

---

## Models
- **Project** — organizes tasks by goal with timeline and automatic completion percentage
- **Task** — single activity with status (today, this week, this month), working on flag and optional project link

---

## Authentication
| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | /api/auth/register/ | Register new user |
| POST | /api/auth/login/ | Get JWT token pair |
| POST | /api/auth/token/refresh/ | Refresh access token |

---

## API Endpoints
| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | /api/projects/ | List user projects |
| POST | /api/projects/ | Create project |
| GET | /api/projects/{id}/ | Project detail with tasks and completion % |
| PUT/PATCH | /api/projects/{id}/ | Update project |
| DELETE | /api/projects/{id}/ | Delete project |
| GET | /api/tasks/ | List user tasks |
| POST | /api/tasks/ | Create task |
| GET | /api/tasks/{id}/ | Task detail |
| PUT/PATCH | /api/tasks/{id}/ | Update task |
| DELETE | /api/tasks/{id}/ | Delete task |

---

## Query Filters
| Parameter | Example | Description |
|-----------|---------|-------------|
| status | ?status=today | Filter by status (today / this_week / this_month) |
| completed | ?completed=true | Completed tasks only |
| is_working_on | ?is_working_on=true | Active tasks only |
| project | ?project=1 | Tasks of a specific project |

---

## Security
- JWT authentication required for all endpoints
- Users can only access and modify their own data
- Double protection: queryset filtering (404) + IsOwner permission (403)

---

## Project Status

| Phase | Description | Status |
|-------|-------------|--------|
| 1 | Models — Project and Task | ✅ |
| 2 | Serializers and CRUD endpoints | ✅ |
| 3 | JWT Authentication | ✅ |
| 4 | IsOwner permission + queryset filtering | ✅ |
| 5 | 17 automated tests — auth, CRUD, ownership | ✅ |
| 6 | Deploy on Railway with PostgreSQL | ✅ |
| 7 | Docker local environment (Django + PostgreSQL + Nginx) | ✅ |

---

## Local Setup

**Standard**
```bash
git clone https://github.com/matteo-cremonini/task-manager-api
cd task-manager-api
cp .env.example .env   # fill in your values
pipenv install
pipenv shell
python manage.py migrate
python manage.py runserver
```

**Docker**
```bash
cp .env.example .env   # fill in your values
docker compose up --build
```

Runs Django + PostgreSQL + Nginx. API available at `http://localhost`.

---

## Running Tests
```bash
python manage.py test
```
