# task-manager-api

REST API for personal task management built with Django REST Framework.

## Tech Stack
- Python 3.12
- Django 6.x
- Django REST Framework
- JWT Authentication (coming soon)
- PostgreSQL (production) / SQLite (development)

## Models
- **Project** — organizes tasks by goal with timeline and automatic completion percentage
- **Task** — single activity with status (today, this week, this month), working on flag and optional project link

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

## Filters
| Parameter | Example | Description |
|-----------|---------|-------------|
| status | ?status=today | Filter by status |
| completed | ?completed=true | Completed tasks only |
| is_working_on | ?is_working_on=true | Active tasks only |
| project | ?project=1 | Tasks of a specific project |

## Status
Phase 2 complete — serializers, ViewSets and filters working.
JWT authentication coming next.

## Local Setup
```bash
git clone https://github.com/matteo-cremonini/task-manager-api
cd task-manager-api
pipenv install
pipenv shell
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```