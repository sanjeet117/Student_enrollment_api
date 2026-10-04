from pydantic import BaseModel


# Student Schemas
class StudentCreate(BaseModel):
    name: str
    email: str


# Course Schemas
class CourseCreate(BaseModel):
    name: str
    description: str | None = None


class CourseResponse(BaseModel):
    id: int
    name: str
    description: str | None = None

    class Config:
        from_attributes = True


# Enrollment Schemas
class EnrollmentCreate(BaseModel):
    student_id: int
    course_id: int


class EnrollmentResponse(BaseModel):
    id: int
    student_id: int
    course_id: int

    class Config:
        from_attributes = True