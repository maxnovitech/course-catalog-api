import os
from typing import Literal, Annotated, Optional
from fastapi import FastAPI, HTTPException, Depends, Query
from fastapi.middleware.cors import CORSMiddleware
from data import find_course, get_all_courses
from models import Course, Stats, Enrollment, EnrollmentIn

app = FastAPI(title="Course Catalog API")

# Bonus Task 3: The origin list from an environment variable (fallback to localhost:3000)
cors_origins = [
    origin.strip()
    for origin in os.getenv("CORS_ORIGINS", "http://localhost:3000").split(",")
    if origin.strip()
]

# Bonus Task 5: Explicit lists instead of asterisks for least privilege security
app.add_middleware(
    CORSMiddleware,
    allow_origins=cors_origins,
    allow_methods=["GET", "POST"],
    allow_headers=["Content-Type"],
)

ENROLLMENTS: list[Enrollment] = []

@app.get("/")
def read_root():
    return {"message": "Course Catalog API is running"}

def pagination(
    page: Annotated[int, Query(ge=1)] = 1,
    page_size: Annotated[int, Query(ge=1, le=100)] = 20
):
    return {"offset": (page - 1) * page_size, "limit": page_size}

@app.get("/courses", response_model=list[Course])
def list_courses(
    is_elective: Optional[bool] = None,
    sort: Literal["popular", "title"] = "popular",
    q: Optional[str] = None,
    p: dict = Depends(pagination),
):
    courses = get_all_courses()

    if q is not None:
        courses = [c for c in courses if q.lower() in c.title.lower()]

    if is_elective is not None:
        courses = [c for c in courses if c.is_elective == is_elective]

    if sort == "title":
        courses = sorted(courses, key=lambda c: c.title)
    else:
        courses = sorted(courses, key=lambda c: c.likes, reverse=True)

    return courses[p["offset"] : p["offset"] + p["limit"]]

@app.get("/courses/{course_id}", response_model=Course)
def get_course(course_id: str):
    course = find_course(course_id)
    if course is None:
        raise HTTPException(status_code=404, detail="Course not found")
    return course

@app.post("/courses/{course_id}/like", response_model=Course)
def like_course(course_id: str):
    course = find_course(course_id)
    if course is None:
        raise HTTPException(status_code=404, detail="Course not found")
    course.likes += 1
    return course

@app.post("/enrollments", response_model=Enrollment, status_code=201)
def create_enrollment(data: EnrollmentIn):
    course = find_course(data.course_id)
    if course is None:
        raise HTTPException(status_code=404, detail="Course not found")
    enrollment = Enrollment(
        id=len(ENROLLMENTS) + 1,
        course_id=data.course_id,
        student_name=data.student_name,
    )
    ENROLLMENTS.append(enrollment)
    return enrollment

@app.get("/enrollments", response_model=list[Enrollment])
def list_enrollments():
    return ENROLLMENTS

@app.get("/stats", response_model=Stats)
def get_stats():
    courses = get_all_courses()
    total = len(courses)
    total_credits = sum(c.credits for c in courses)
    electives = sum(1 for c in courses if c.is_elective)
    return Stats(total=total, total_credits=total_credits, electives=electives)
