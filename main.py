from typing import Literal, Annotated, Optional
from fastapi import FastAPI, HTTPException, Depends, Query
from data import find_course, get_all_courses
from models import Course, Stats

app = FastAPI(title="Course Catalog API")

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

@app.get("/stats", response_model=Stats)
def get_stats():
    courses = get_all_courses()
    total = len(courses)
    total_credits = sum(c.credits for c in courses)
    electives = sum(1 for c in courses if c.is_elective)
    return Stats(total=total, total_credits=total_credits, electives=electives)
