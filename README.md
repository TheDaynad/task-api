# Task API

## About

A REST API for managing users and tasks, built with FastAPI and PostgreSQL.

## Tech Stack

- Python
- FastAPI
- PostgreSQL
- SQLAlchemy 2 (Async)
- Alembic
- Redis
- Docker Compose

## Features

The project provides CRUD operations for users and tasks.

Users can:
- Create a user
- Get a list of users
- Get a user by ID
- Update a user
- Partially update a user
- Delete a user

Tasks can:
- Create a task
- Get a list of tasks
- Get a task by ID
- Get tasks for a specific user
- Update a task
- Partially update a task
- Delete a task

The API returns a `404 Not Found` error when a requested user or task does not exist.

## Redis Caching

Redis is used as a caching layer to reduce unnecessary database queries.

Implemented features:
- Cache task lists using the `tasks:list` key.
- Cache individual tasks using keys such as `task:1`.
- Set a TTL of 300 seconds for cached data.
- Invalidate relevant cache keys after creating, updating, or deleting tasks.
- Handle Redis errors gracefully and fall back to PostgreSQL when Redis is unavailable.

PostgreSQL remains the primary data source. Redis is an auxiliary service.

## API Endpoints

### Users

| Method | Endpoint | Description |
|---|---|---|
| `POST` | `/users` | Create a user |
| `GET` | `/users` | Get all users |
| `GET` | `/users/{user_id}` | Get a user by ID |
| `PUT` | `/users/{user_id}` | Update a user |
| `PATCH` | `/users/{user_id}` | Partially update a user |
| `DELETE` | `/users/{user_id}` | Delete a user |

### Tasks

| Method | Endpoint | Description |
|---|---|---|
| `POST` | `/tasks` | Create a task |
| `GET` | `/tasks` | Get all tasks |
| `GET` | `/tasks/{task_id}` | Get a task by ID |
| `GET` | `/users/{user_id}/tasks` | Get all tasks for a specific user |
| `PUT` | `/tasks/{task_id}` | Update a task |
| `PATCH` | `/tasks/{task_id}` | Partially update a task |
| `DELETE` | `/tasks/{task_id}` | Delete a task |

## Installation and Run

### Prerequisites

- Docker Desktop
- Git

### Clone the repository

```bash
git clone https://github.com/TheDaynad/task-api.git
cd task-api
```

### Configure environment variables

Create a local environment file from the example:

**Windows PowerShell:**
```powershell
Copy-Item .env.example .env
```

**Linux / macOS:**
```bash
cp .env.example .env
```

Update the values in `.env` if needed.

Make sure `REDIS_URL` is configured:

```env
REDIS_URL=redis://redis:6379/0
```

### Start the application

```bash
docker compose up --build -d
```

### Apply database migrations

```bash
docker compose exec api alembic upgrade head
```

### Open API documentation

Swagger UI:

http://localhost:8000/docs

