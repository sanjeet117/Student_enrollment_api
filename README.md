# Student Course Enrollment API

A FastAPI-based REST API for managing students, courses, and course enrollments using PostgreSQL and SQLAlchemy.

## Project Overview

This project provides APIs to:

- Create students
- Create courses
- View all courses
- Enroll students in courses
- View courses enrolled by a student
- Delete enrollments
- Prevent duplicate enrollment
- Handle invalid student and course IDs with meaningful errors

## Technologies Used

- Python
- FastAPI
- Uvicorn
- SQLAlchemy
- PostgreSQL
- Neon PostgreSQL
- Pydantic
- Psycopg
- Python Dotenv
- Swagger UI

## Project Architecture

```text
Client / Swagger UI
        |
        v
     FastAPI
        |
        v
    SQLAlchemy
        |
        v
Neon PostgreSQL
```

## Project Structure

```text
student_course_api/
│
├── .env
├── .gitignore
├── database.py
├── main.py
├── model.py
├── schemas.py
├── tables.py
├── requirements.txt
└── README.md
```

## File Description

### main.py

Contains the FastAPI application and API endpoints.

### database.py

Handles the PostgreSQL database connection and SQLAlchemy database session.

### model.py

Contains SQLAlchemy ORM models for:

- Student
- Course
- Enrollment

### schemas.py

Contains Pydantic schemas used for request validation and API responses.

### tables.py

Creates the database tables using SQLAlchemy metadata.

### requirements.txt

Contains the Python packages required to run the project.

### .env

Stores the PostgreSQL database connection string.

The `.env` file should not be committed to GitHub.

## Database Tables

### Students

Stores student information.

Fields:

- id
- name
- email

### Courses

Stores course information.

Fields:

- id
- name
- description

### Enrollments

Connects students with courses.

Fields:

- id
- student_id
- course_id

The enrollment table uses foreign keys to connect students and courses.

## API Endpoints

| Method | Endpoint | Description |
|---|---|---|
| GET | `/` | Check whether the API is running |
| POST | `/students` | Create a student |
| POST | `/courses` | Create a course |
| GET | `/courses` | Get all courses |
| POST | `/enroll` | Enroll a student in a course |
| GET | `/students/{student_id}/courses` | Get courses enrolled by a student |
| DELETE | `/enroll/{enrollment_id}` | Delete an enrollment |

## API Testing

The project uses FastAPI's automatically generated Swagger UI.

After starting the application, open:

```text
http://127.0.0.1:8000/docs
```

Swagger UI can be used to test all APIs directly from the browser.

## Example: Create Student

### Request

```http
POST /students
```

```json
{
  "name": "Rahul",
  "email": "rahul@example.com"
}
```

## Example: Create Course

### Request

```http
POST /courses
```

```json
{
  "name": "Python Programming",
  "description": "Learn Python programming fundamentals"
}
```

## Example: Enroll Student

### Request

```http
POST /enroll
```

```json
{
  "student_id": 1,
  "course_id": 3
}
```

This enrolls student ID 1 in course ID 3.

## Duplicate Enrollment Prevention

The API checks whether the student is already enrolled in the requested course.

If the same enrollment is attempted again, the API returns:

```text
400 Bad Request
```

Example response:

```json
{
  "detail": "Student is already enrolled in this course"
}
```

## Error Handling

The API provides meaningful HTTP errors.

### Student Not Found

```text
404 Not Found
```

```json
{
  "detail": "Student not found"
}
```

### Course Not Found

```text
404 Not Found
```

```json
{
  "detail": "Course not found"
}
```

### Enrollment Not Found

```text
404 Not Found
```

```json
{
  "detail": "Enrollment not found"
}
```

## Installation

### 1. Clone the repository

```bash
git clone <your-github-repository-url>
```

### 2. Move into the project directory

```bash
cd student_course_api
```

### 3. Create a virtual environment

```bash
python -m venv venv
```

### 4. Activate the virtual environment

For Windows PowerShell:

```powershell
.\venv\Scripts\Activate.ps1
```

If PowerShell execution policy prevents activation:

```powershell
Set-ExecutionPolicy -ExecutionPolicy Bypass -Scope Process
```

Then:

```powershell
.\venv\Scripts\Activate.ps1
```

### 5. Install dependencies

```powershell
pip install -r requirements.txt
```

## Environment Configuration

Create a `.env` file in the project root:

```text
DATABASE_URL=YOUR_NEON_DATABASE_CONNECTION_STRING
```

Do not upload the `.env` file to GitHub.

## Create Database Tables

Run:

```powershell
python tables.py
```

Expected output:

```text
Tables created successfully!
```

## Run the Application

Start the FastAPI application:

```powershell
uvicorn main:app --reload
```

The application will run at:

```text
http://127.0.0.1:8000
```

Swagger documentation:

```text
http://127.0.0.1:8000/docs
```

## Database

This project uses Neon PostgreSQL as the database.

SQLAlchemy is used as the ORM layer between FastAPI and PostgreSQL.

```text
FastAPI
   |
   v
SQLAlchemy ORM
   |
   v
Neon PostgreSQL
```

## Key Features

- REST API development using FastAPI
- PostgreSQL database integration
- SQLAlchemy ORM
- Pydantic request validation
- Dependency injection using `Depends`
- CRUD operations
- Foreign key relationships
- Duplicate enrollment prevention
- HTTP exception handling
- Swagger API documentation

## Author

Sanjeet Kumar