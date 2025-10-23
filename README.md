# taller-challenge
Code Challenge for Senior Python Fullstack Engineer

### Challenge
Build a Scalable FastAPI Backend Service with PostgreSQL Integration

### Scenario
You are tasked with building a simple backend service for managing "Projects" and their associated "Tasks". Each Project can have multiple Tasks. The service should expose RESTful APIs to create, read, update, and delete Projects and Tasks. Additionally, implement an endpoint to retrieve all Tasks for a given Project, sorted by their priority.

### Requirements

#### Backend API

Use FastAPI to build the RESTful API.

Implement the following endpoints:

- `POST` /projects/ — Create a new project
- `GET` /projects/{project_id} — Retrieve project details
- `PUT` /projects/{project_id} — Update project details
- `DELETE` /projects/{project_id} — Delete a project
- `POST` /projects/{project_id}/tasks/ — Add a new task to a project
- `GET` /projects/{project_id}/tasks/ — List all tasks for a project, sorted by priority (descending)
- `PUT` /tasks/{task_id} — Update a task
- `DELETE` /tasks/{task_id} — Delete a task

#### Data Model

Project

- `id`: UUID or int
- `name`: string (required)
- `description`: string (optional)
- `created_at`: timestamp

Task

- `id`: UUID or int
- `project_id`: foreign key to Project
- `title`: string (required)
- `priority`: integer (higher number = higher priority)
- `completed`: boolean (default False)
- `due_date`: date (optional)

#### Database

Use PostgreSQL for data persistence.

Design an efficient schema with appropriate indexes (e.g., on `project_id` and `priority`).

Write optimized queries to fetch tasks sorted by priority.

#### Additional Requirements

- Use asynchronous endpoints and database calls (e.g., with asyncpg or the `databases` library)
- Validate input data using Pydantic models
- Handle errors gracefully (e.g., 404 for not found, 400 for invalid input)
- Write clean, maintainable, and well-structured code

### ⭐️ Bonus (if time permits)

- Implement simple authentication (e.g., API key header) to protect the endpoints
- Add pagination support to the GET /projects/{project_id}/tasks/ endpoint

**Constraints & Resources**

Duration: 25-30 minutes.

### External Resources

- Use a free PostgreSQL instance locally or via ElephantSQL (free tier)
- FastAPI documentation: https://fastapi.tiangolo.com/

Async database libraries:

- databases (https://www.encode.io/databases/)
- asyncpg (https://magicstack.github.io/asyncpg/current/)

Environment: Candidate can use any IDE or online environment supporting Python 3.8+ and PostgreSQL.

## How to Run

This project is containerized using **Docker Compose**.

### Quick Start
```bash
docker-compose up --build
```
This will start:
- **FastAPI** application (located in `src/app`)
- **PostgreSQL** database instance (configured via `docker-compose.yml`)

You can access the API once it’s running at:
👉 http://localhost:8000/docs

## Authentication

This API implements JWT (JSON Web Token) based authentication with Bearer tokens.

### Quick Start Authentication

1. **Default Credentials**:
   - Username: `admin`
   - Password: `1234`

2. **Get JWT Token**:
   ```bash
   curl -X POST "http://localhost:8000/api/v1/auth/login" \
        -H "Content-Type: application/json" \
        -d '{"username": "admin", "password": "1234"}'
   ```

3. **Use Token in Requests**:
   ```bash
   curl -X GET "http://localhost:8000/api/v1/auth/me" \
        -H "Authorization: Bearer YOUR_JWT_TOKEN_HERE"
   ```
