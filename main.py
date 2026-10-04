from fastapi import FastAPI, Depends, status, HTTPException
from sqlalchemy.orm import Session

import model
import schemas

from database import engine, get_db


# Create database tables
model.Base.metadata.create_all(bind=engine)


# Create FastAPI application
app = FastAPI(
    title="Student Course Enrollment API",
    description="API for managing students, courses and enrollments",
    version="1.0.0"
)


# Home API
@app.get("/")
def home():
    return {
        "message": "Student Course Enrollment API is running"
    }


# Create Student
@app.post(
    "/students",
    status_code=status.HTTP_201_CREATED
)
def create_student(
    student: schemas.StudentCreate,
    db: Session = Depends(get_db)
):

    # Check whether email already exists
    existing_student = db.query(model.Student).filter(
        model.Student.email == student.email
    ).first()

    if existing_student:
        raise HTTPException(
            status_code=400,
            detail="Student with this email already exists"
        )

    new_student = model.Student(
        name=student.name,
        email=student.email
    )

    db.add(new_student)
    db.commit()
    db.refresh(new_student)

    return new_student


# Create Course
@app.post(
    "/courses",
    response_model=schemas.CourseResponse,
    status_code=status.HTTP_201_CREATED
)
def create_course(
    course: schemas.CourseCreate,
    db: Session = Depends(get_db)
):

    new_course = model.Course(
        name=course.name,
        description=course.description
    )

    db.add(new_course)
    db.commit()
    db.refresh(new_course)

    return new_course


# Get All Courses
@app.get(
    "/courses",
    response_model=list[schemas.CourseResponse]
)
def get_courses(
    db: Session = Depends(get_db)
):

    courses = db.query(model.Course).all()

    return courses


# Enroll Student in Course
@app.post(
    "/enroll",
    response_model=schemas.EnrollmentResponse,
    status_code=status.HTTP_201_CREATED
)
def enroll_student(
    enrollment: schemas.EnrollmentCreate,
    db: Session = Depends(get_db)
):

    # Check whether student exists
    student = db.query(model.Student).filter(
        model.Student.id == enrollment.student_id
    ).first()

    if not student:
        raise HTTPException(
            status_code=404,
            detail="Student not found"
        )

    # Check whether course exists
    course = db.query(model.Course).filter(
        model.Course.id == enrollment.course_id
    ).first()

    if not course:
        raise HTTPException(
            status_code=404,
            detail="Course not found"
        )

    # Check duplicate enrollment
    existing_enrollment = db.query(model.Enrollment).filter(
        model.Enrollment.student_id == enrollment.student_id,
        model.Enrollment.course_id == enrollment.course_id
    ).first()

    if existing_enrollment:
        raise HTTPException(
            status_code=400,
            detail="Student is already enrolled in this course"
        )

    # Create new enrollment
    new_enrollment = model.Enrollment(
        student_id=enrollment.student_id,
        course_id=enrollment.course_id
    )

    db.add(new_enrollment)
    db.commit()
    db.refresh(new_enrollment)

    return new_enrollment


# Get Student's Courses
@app.get(
    "/students/{student_id}/courses",
    response_model=list[schemas.CourseResponse]
)
def get_student_courses(
    student_id: int,
    db: Session = Depends(get_db)
):

    # Check whether student exists
    student = db.query(model.Student).filter(
        model.Student.id == student_id
    ).first()

    if not student:
        raise HTTPException(
            status_code=404,
            detail="Student not found"
        )

    # Get all enrollments for student
    enrollments = db.query(model.Enrollment).filter(
        model.Enrollment.student_id == student_id
    ).all()

    # Get courses from enrollments
    courses = [
        enrollment.course
        for enrollment in enrollments
    ]

    return courses


# Delete Enrollment
@app.delete(
    "/enroll/{enrollment_id}"
)
def delete_enrollment(
    enrollment_id: int,
    db: Session = Depends(get_db)
):

    # Find enrollment
    enrollment = db.query(model.Enrollment).filter(
        model.Enrollment.id == enrollment_id
    ).first()

    # Enrollment does not exist
    if not enrollment:
        raise HTTPException(
            status_code=404,
            detail="Enrollment not found"
        )

    # Delete enrollment
    db.delete(enrollment)
    db.commit()

    return {
        "message": "Enrollment deleted successfully"
    }

