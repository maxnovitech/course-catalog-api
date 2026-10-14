from fastapi.testclient import TestClient
from main import app, ENROLLMENTS
from data import COURSES

client = TestClient(app)

def setup_function():
    ENROLLMENTS.clear()

def test_root():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Course Catalog API is running"}

def test_cors_headers():
    response = client.get("/", headers={"Origin": "http://localhost:3000"})
    assert response.status_code == 200
    assert response.headers.get("access-control-allow-origin") == "http://localhost:3000"

    foreign = client.get("/", headers={"Origin": "http://evil.example"})
    assert "access-control-allow-origin" not in foreign.headers

def test_camel_case_courses():
    response = client.get("/courses")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 6
    first = data[0]
    # Check camelCase keys
    assert "isElective" in first
    assert "is_elective" not in first

def test_query_param_is_elective():
    response = client.get("/courses?is_elective=true")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 2
    for c in data:
        assert c["isElective"] is True

def test_like_course():
    # web-security initial likes in data.py is 21
    res = client.post("/courses/web-security/like")
    assert res.status_code == 200
    assert res.json()["id"] == "web-security"
    likes = res.json()["likes"]

    res2 = client.post("/courses/web-security/like")
    assert res2.status_code == 200
    assert res2.json()["likes"] == likes + 1

    res_404 = client.post("/courses/nope/like")
    assert res_404.status_code == 404
    assert res_404.json()["detail"] == "Course not found"

def test_enrollment_lifecycle():
    # Valid enrollment
    res = client.post("/enrollments", json={"courseId": "web-security", "studentName": "Aigerim"})
    assert res.status_code == 201
    data = res.json()
    assert data["id"] == 1
    assert data["courseId"] == "web-security"
    assert data["studentName"] == "Aigerim"

    # Listing enrollments
    res_list = client.get("/enrollments")
    assert res_list.status_code == 200
    assert len(res_list.json()) == 1
    assert res_list.json()[0]["studentName"] == "Aigerim"

    # Validation: short name (< 2 chars) -> 422
    res_short = client.post("/enrollments", json={"courseId": "web-security", "studentName": "A"})
    assert res_short.status_code == 422
    assert res_short.json()["detail"][0]["loc"] == ["body", "studentName"]

    # Unknown course -> 404
    res_404 = client.post("/enrollments", json={"courseId": "nope", "studentName": "Aigerim"})
    assert res_404.status_code == 404
