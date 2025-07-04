 STUDENT ASSESSMENT & REPORTING SYSTEM - DJANGO BACKEND

A Django RESTful API for managing Teachers, Students, Assessments, Scores, Progress Reports, and Admin functions.

=======================================================================
FEATURES
=======================================================================

1. USER AUTHENTICATION (JWT Based)
------------------------------------
- Register and login teachers securely.
- Uses JWT token for session validation.

▶️ REGISTER (POST): http://127.0.0.1:8000/api/register/

Request:
{
"username": "PythonTeachers",
"email": "Pythonteacher@gmail.com",
"password": "PythonTeacher979@@12345&&@#$"
}

Response:
{
"message": "Teacher registered successfully"
}


▶️ LOGIN (POST): http://127.0.0.1:8000/api/login/

Request:
{
"username": "PythonTeachers",
"password": "PythonTeacher979@@12345&&@#$"
}

Response:
{
"token": "eyJhbGciOiJIUzI1NiIsInR5cCI6..."
}


2. STUDENT MANAGEMENT
--------------------------
- Add, Edit, Delete students
- Assign class & section
- View with filters, pagination

▶️ ADD STUDENT (POST): /api/students/

Request:
{
"name": "ArunGopal",
"class_name": "8th",
"section": "A"
}

Response:
{
"message": "Student created",
"id": 22
}


▶️ GET ALL STUDENTS (GET): /api/students/

Response:
[
{
"id": 10,
"name": "Teliva",
"class_name": "11th",
"section": "C"
},
...
]


▶️ UPDATE STUDENT (PUT): /api/students/

Request:
{
"id": 21,
"name": "John",
"class_name": "2nd class",
"section": "B"
}

Response:
{
"message": "Student updated"
}


▶️ DELETE STUDENT (DELETE): /api/students/

Request:
{
"id": 21
}

Response:
{
"message": "Student deleted"
}


▶️ PAGINATION + FILTER (GET): /api/students/list/?class=7th&section=A&page=1

Response:
{
"total": 1,
"pages": 1,
"current": 1,
"students": [
{
"id": 5,
"name": "Govind",
"class_name": "7th",
"section": "A"
}
]
}


3. ASSESSMENTS MODULE
--------------------------
- Create assessments chapter-wise
- Assign scores weekly
- View/update historical data

▶️ CREATE ASSESSMENT (POST): /api/assessments/

Request:
{
"title": "Weekly Test",
"chapter": "Integration Maths",
"week": 4,
"total_marks": 80
}

Response:
{
"message": "Assessment created",
"id": 7
}


▶️ VIEW ASSESSMENTS (GET): /api/assessments/

Response:
[
{
"id": 1,
"title": "Weekly Test",
"chapter": "Algebra",
"week": 1,
"total_marks": 50
},
...
]


4. ASSIGN SCORES TO STUDENTS
----------------------------------
▶️ ADD SCORE (POST): /api/scores/

Request:
{
"student_id": 5,
"assessment_id": 6,
"marks": 40
}

Response:
{
"message": "Score added successfully."
}


▶️ VIEW ALL SCORES (GET): /api/scores/

Response:
[
{
"id": 1,
"student_id": 2,
"assessment_id": 1,
"marks": 45
},
...
]


5. WEEKLY PROGRESS TRACKING
-------------------------------------
▶️ WEEKLY SCORECARD (GET): /api/progress/5/

Response:
[
{
"assessment__week": 4,
"assessment__title": "Weekly Test",
"assessment__total_marks": 80,
"marks": 46
},
...
]


▶️ STUDENT REPORT (GET): /api/report/5/

Response:
{
"student": "Govind",
"report": [
{
"id": 1,
"assessment": "Weekly Test",
"chapter": "Integration Maths",
"week": 4,
"marks_obtained": 42,
"total_marks": 80,
"percentage": 52.5
},
...
],
"total_marks_obtained": 183,
"total_marks_possible": 300,
"overall_percentage": 61
}


6. ADMIN PANEL
-------------------
- Login to Django admin to manage teachers, students, assessments
- Roles handled: Admin, Teacher


=======================================================================
TECH STACK
=======================================================================
- Backend: Django (Python)
- Database: SQLite (easily upgradable to PostgreSQL/MySQL)
- Auth: JWT (Custom Token)
- API Testing: Postman
- Pagination: Paginator
- Deployment Ready: Yes (Render, Railway, Heroku etc.)

=======================================================================
SETUP INSTRUCTIONS
=======================================================================

1. Clone the repository:
git clone https://github.com/GaneshSharma9989/SPTS_BACKEND

2. Navigate to the project:
cd spts_backend

3. Create virtual environment:
python -m venv venv

4. Activate the environment:
Windows: venv\Scripts\activate
macOS/Linux: source venv/bin/activate

5. Install dependencies:
pip install -r requirements.txt

6. Apply migrations:
python manage.py migrate

7. Run the development server:
python manage.py runserver

=======================================================================
 (Important Notes)
=======================================================================
✔ Only GET methods will show response in browser; POST/PUT/DELETE must be tested in Postman or via frontend.
✔ Token is required for protected endpoints (pass in headers: `Authorization: Bearer <token>`).
✔ Pagination improves performance when fetching long student lists.
✔ Django Admin panel is available at `/admin/` (only for admin users).
✔ CSRF disabled temporarily for testing (`@csrf_exempt`). Must be handled in production.

=======================================================================
CONTACT
=======================================================================
👨‍💻 Ganesh Sharma
📂 GitHub: https://github.com/GaneshSharma9989
📧 Email: ganesh17324@gmail.com 


