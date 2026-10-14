# Course Catalog API

Novikov Maxim IT3-2304

A standalone backend project for a course catalog built with FastAPI and Pydantic. Updated for Lab 5 with CORS integration, camelCase JSON contract, like mutation, and course enrollments.

## How to run

1. Create a virtual environment:
   ```bash
   python3 -m venv .venv
   source .venv/bin/activate  # macOS/Linux
   # or .venv\Scripts\Activate.ps1 on Windows
   ```
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Start the dev server:
   ```bash
   fastapi dev main.py
   ```
   The API will be available at `http://127.0.0.1:8000`. Interactive documentation is available at `http://127.0.0.1:8000/docs`.

---

## What changed (Lab 5)

### 1. Allowed Origin (CORS)
- **Why it's needed**: By default, web browsers enforce the Same-Origin Policy (SOP). When a frontend running at `http://localhost:3000` makes requests to `http://localhost:8000` via JavaScript (`fetch`/SWR), the browser blocks client code from reading the response unless the server explicitly grants permission via the `Access-Control-Allow-Origin: http://localhost:3000` header.
- **Implementation**: Added `CORSMiddleware` to FastAPI.
- **Bonus 3 & Bonus 5**: Configured dynamic origin reading via `CORS_ORIGINS` (defaulting to `http://localhost:3000`) and explicit whitelist for methods `["GET", "POST"]` and headers `["Content-Type"]`.

### 2. camelCase in JSON
- **Why it's needed**: Python conventions use `snake_case` (e.g. `is_elective`, `student_name`), while JavaScript / TypeScript conventions and frontend models expect `camelCase` (e.g. `isElective`, `studentName`).
- **Implementation**: Introduced `CamelModel(BaseModel)` with `ConfigDict(alias_generator=to_camel, validate_by_name=True, validate_by_alias=True)`. All models (`Course`, `Stats`, `EnrollmentIn`, `Enrollment`) inherit from `CamelModel`.
- **Query parameters**: Remain `snake_case` (`?is_elective=true`) because aliases apply only to request and response bodies.

### 3. New Routes and Example Responses

#### `POST /courses/{course_id}/like`
- Increments the `likes` counter for the specified course in memory.
- If course doesn't exist, returns `404 Not Found`.
- **Response (200 OK)**:
```json
{
  "id": "web-security",
  "title": "Web Security Essentials",
  "description": "JWT/OAuth2, XSS, CSRF, and SQL injection defense.",
  "credits": 4,
  "isElective": false,
  "likes": 22
}
```

#### `POST /enrollments`
- Accepts an enrollment JSON body validated by `EnrollmentIn` (`course_id: str`, `student_name: str` with minimum 2 characters).
- If course does not exist: returns `404 Course not found`.
- If student name length < 2: returns `422 Unprocessable Entity` with validation detail.
- **Request Body**:
```json
{
  "courseId": "web-security",
  "studentName": "Aigerim"
}
```
- **Response (201 Created)**:
```json
{
  "id": 1,
  "courseId": "web-security",
  "studentName": "Aigerim"
}
```

#### `GET /enrollments`
- Returns all enrolled students from the in-memory store.
- **Response (200 OK)**:
```json
[
  {
    "id": 1,
    "courseId": "web-security",
    "studentName": "Aigerim"
  }
]
```

---

## What was verified

The following requests were verified against the API:

| Request | Expected result |
| --- | --- |
| `/` | `{"message": "Course Catalog API is running"}` |
| `/courses` | 6 courses; `ai-integration` first (32 likes), `api-design` last (11); keys in camelCase (`isElective`) |
| `/courses?is_elective=true` | 2 courses: `ai-integration`, `api-design` |
| `/courses?is_elective=false` | 4 courses: `modern-frontend`, `web-security`, `backend-fastapi`, `databases-postgresql` |
| `/courses?sort=title` | 6 courses alphabetically by title |
| `/courses?page=1&page_size=2` | `ai-integration`, `modern-frontend` |
| `/courses?page=2&page_size=2` | `web-security`, `backend-fastapi` |
| `/courses?page=3&page_size=2` | `databases-postgresql`, `api-design` |
| `/courses?page=4&page_size=2` | an empty list `[]` |
| `/courses/web-security` | returns the "web-security" course |
| `/courses/nope` | returns a 404 code with the body `{"detail": "Course not found"}` |
| `POST /courses/web-security/like` | increments likes and returns updated course |
| `POST /courses/nope/like` | 404 `{"detail": "Course not found"}` |
| `POST /enrollments` (valid) | 201 Created with `{ "id": 1, "courseId": "...", "studentName": "..." }` |
| `POST /enrollments` (`studentName: "A"`) | 422 Unprocessable Entity (`String should have at least 2 characters`) |
| `POST /enrollments` (`courseId: "nope"`) | 404 `{"detail": "Course not found"}` |
| `GET /enrollments` | returns list of enrolled records |
| `/stats` (Bonus) | returns `{"total": 6, "totalCredits": 28, "electives": 2}` |
| `/courses?q=react` (Bonus) | returns `modern-frontend` |
| Preflight `OPTIONS /enrollments` | 200 OK with `access-control-allow-origin: http://localhost:3000` |
| Preflight `OPTIONS` with `DELETE` | 400 Bad Request (`Disallowed CORS method`) |

---

## Testing

Run the automated test suite with pytest:
```bash
pytest test_fastapi.py
```
All 7 unit and integration tests pass.
