# Course Catalog API

Novikov Maxim IT3-2304

A standalone backend project for a course catalog built with FastAPI and Pydantic.

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
   The API will be available at http://127.0.0.1:8000. Interactive documentation is available at http://127.0.0.1:8000/docs.

## What was verified

The following requests were verified against the API:

| Request | Expected result |
| --- | --- |
| `/courses` | 6 courses; ai-integration first (32 likes), api-design last (11) |
| `/courses?is_elective=true` | 2 courses: ai-integration, api-design |
| `/courses?is_elective=false` | 4 courses: modern-frontend, web-security, backend-fastapi, databases-postgresql |
| `/courses?sort=title` | 6 courses alphabetically by title: ai-integration, api-design, backend-fastapi, modern-frontend, databases-postgresql, web-security |
| `/courses?page=1&page_size=2` | ai-integration, modern-frontend |
| `/courses?page=2&page_size=2` | web-security, backend-fastapi |
| `/courses?page=3&page_size=2` | databases-postgresql, api-design |
| `/courses?page=4&page_size=2` | an empty list `[]` |
| `/courses` (pagination defaults)| all 6 courses (page_size defaults to 20) |
| `/courses/web-security` | returns the "web-security" course |
| `/courses/nope` | returns a 404 code with the body `{"detail": "Course not found"}` |
| `/stats` (Bonus) | returns `{"total": 6, "total_credits": 28, "electives": 2}` |
| `/courses?q=react` (Bonus) | returns modern-frontend |




  ### General & Setup

  1. What is the purpose of this project?
  It's a standalone backend API for a university or school course catalog, built using Python, FastAPI, and Pydantic. It
  looks like an educational lab or assignment.

  2. How do I run the application locally?
  Create a Python virtual environment, install the required packages using pip install -r requirements.txt, and start
  the development server by running fastapi dev main.py.

  3. Where can I find the API documentation?
  Once the server is running, you can access the interactive, automatically generated Swagger UI documentation by
  navigating to http://127.0.0.1:8000/docs in your browser.

  4. What kind of database is this project using?
  There is no external database. The data is hardcoded and stored in memory as a static list inside the data.py file.

  ### Features & Endpoints

  5. What endpoints are available in this API?

  • /: Returns a simple message confirming the API is running.
  • /courses: Returns a list of courses.
  • /courses/{course_id}: Returns the details of a specific course.
  • /stats: Returns a summary of the catalog (total courses, total credits, elective count).

  6. How can I search or filter the courses?
  You can use query parameters on the /courses endpoint. For example, ?is_elective=true filters for elective courses,
  and ?q=react searches for courses containing "react" in their title.

  7. Does the API support sorting?
  Yes. By default, courses are sorted by popularity (likes). You can change this to alphabetical order by title using
  the query parameter ?sort=title.

  8. Is there pagination for the courses list?
  Yes. You can paginate the list using page and page_size query parameters (e.g., ?page=2&page_size=2). The default is
  page 1 with 20 items per page.

  ### Error Handling & Under the Hood

  9. What happens if I request a course ID that doesn't exist?
  If you try to access an invalid course (e.g., /courses/nope), the API will return an HTTP 404 Not Found error with the
  message {"detail": "Course not found"}.

  10. How is the data validated and structured?
  The API uses Pydantic models (specifically the Course and Stats classes in models.py) to define what the data should
  look like. FastAPI automatically uses these models to validate inputs and format the JSON responses.

  11. How can I test that everything is working?
  The project includes a test_fastapi.py file which contains automated tests to verify the routing, pagination,
  filtering, and error handling. You can run these using a testing framework like pytest.
