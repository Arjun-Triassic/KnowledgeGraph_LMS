# KnowledgeGraph LMS - Complete API Documentation

Complete API reference with endpoints, request/response payloads, and examples.

**Base URL**: `http://127.0.0.1:8000`

**Authentication**: All endpoints require `X-User-Id` header with a valid user ID.

**Interactive Docs**: http://127.0.0.1:8000/docs

---

## Table of Contents

1. [Users API](#users-api)
2. [Courses API](#courses-api)
3. [Modules API](#modules-api)
4. [Lessons API](#lessons-api)
5. [Assessments API](#assessments-api)
6. [Enrollments API](#enrollments-api)
7. [Submissions API](#submissions-api)

---

## Users API

### Create User

**POST** `/users/`

**Permissions**: Admin only

**Request Headers**:
```
X-User-Id: <admin_user_id>
Content-Type: application/json
```

**Request Body**:
```json
{
  "email": "user@example.com",
  "first_name": "John",
  "last_name": "Doe",
  "role": "learner"
}
```

**Valid Roles**: `admin`, `instructor`, `learner`

**Response** (201 Created):
```json
{
  "id": 2,
  "email": "user@example.com",
  "first_name": "John",
  "last_name": "Doe",
  "role": "learner",
  "created_at": "2025-12-17T10:00:00Z"
}
```

**cURL Example**:
```bash
curl -X 'POST' \
  'http://127.0.0.1:8000/users/' \
  -H 'X-User-Id: 1' \
  -H 'Content-Type: application/json' \
  -d '{
    "email": "instructor@example.com",
    "first_name": "Jane",
    "last_name": "Smith",
    "role": "instructor"
  }'
```

---

### List Users

**GET** `/users/`

**Permissions**: Authenticated users

**Request Headers**:
```
X-User-Id: <user_id>
```

**Query Parameters**:
- `offset` (int, optional): Pagination offset (default: 0)
- `limit` (int, optional): Results per page (default: 100)

**Response** (200 OK):
```json
[
  {
    "id": 1,
    "email": "admin@example.com",
    "first_name": "Admin",
    "last_name": "User",
    "role": "admin",
    "created_at": "2025-12-17T09:00:00Z"
  },
  {
    "id": 2,
    "email": "user@example.com",
    "first_name": "John",
    "last_name": "Doe",
    "role": "learner",
    "created_at": "2025-12-17T10:00:00Z"
  }
]
```

**cURL Example**:
```bash
curl -X 'GET' \
  'http://127.0.0.1:8000/users/?offset=0&limit=10' \
  -H 'X-User-Id: 1'
```

---

### Get User by ID

**GET** `/users/{user_id}`

**Permissions**: Authenticated users

**Response** (200 OK):
```json
{
  "id": 2,
  "email": "user@example.com",
  "first_name": "John",
  "last_name": "Doe",
  "role": "learner",
  "created_at": "2025-12-17T10:00:00Z"
}
```

---

### Update User

**PUT** `/users/{user_id}`

**Permissions**: Admin only

**Request Body** (all fields optional):
```json
{
  "first_name": "Johnny",
  "last_name": "Doe",
  "role": "instructor"
}
```

**Response** (200 OK): Updated user object

---

### Delete User

**DELETE** `/users/{user_id}`

**Permissions**: Admin only

**Response** (204 No Content)

---

## Courses API

### Create Course

**POST** `/courses/`

**Permissions**: Admin, Instructor

**Request Body**:
```json
{
  "title": "Introduction to Python Programming",
  "description": "Learn Python from scratch with hands-on exercises and projects",
  "category": "Programming",
  "instructor_id": 2
}
```

**Note**: `instructor_id` is optional. Can be assigned later.

**Response** (201 Created):
```json
{
  "id": 1,
  "title": "Introduction to Python Programming",
  "description": "Learn Python from scratch with hands-on exercises and projects",
  "category": "Programming",
  "instructor_id": 2,
  "prerequisite_ids": []
}
```

**cURL Example**:
```bash
curl -X 'POST' \
  'http://127.0.0.1:8000/courses/' \
  -H 'X-User-Id: 1' \
  -H 'Content-Type: application/json' \
  -d '{
    "title": "Advanced Data Structures",
    "description": "Deep dive into trees, graphs, and algorithms",
    "category": "Computer Science",
    "instructor_id": 2
  }'
```

---

### List Courses

**GET** `/courses/`

**Query Parameters**:
- `offset` (int, default: 0)
- `limit` (int, default: 100)

**Response** (200 OK):
```json
[
  {
    "id": 1,
    "title": "Introduction to Python Programming",
    "description": "Learn Python from scratch...",
    "category": "Programming",
    "instructor_id": 2,
    "prerequisite_ids": []
  }
]
```

---

### Get Course by ID

**GET** `/courses/{course_id}`

**Response** (200 OK): Course object with prerequisite_ids

---

### Update Course

**PUT** `/courses/{course_id}`

**Permissions**: Admin, Instructor

**Request Body** (all fields optional):
```json
{
  "title": "Advanced Python Programming",
  "description": "Updated description",
  "category": "Programming",
  "instructor_id": 3
}
```

---

### Delete Course

**DELETE** `/courses/{course_id}`

**Permissions**: Admin only

**Response** (204 No Content)

---

### Assign Instructor

**POST** `/courses/{course_id}/assign-instructor/{instructor_id}`

**Permissions**: Admin only

**Response** (200 OK): Updated course object

**cURL Example**:
```bash
curl -X 'POST' \
  'http://127.0.0.1:8000/courses/1/assign-instructor/2' \
  -H 'X-User-Id: 1'
```

---

### Set Prerequisites

**POST** `/courses/{course_id}/prerequisites`

**Permissions**: Admin, Instructor

**Request Body**:
```json
{
  "prerequisite_ids": [2, 3, 5]
}
```

**Response** (200 OK): Course with updated prerequisites

**cURL Example**:
```bash
curl -X 'POST' \
  'http://127.0.0.1:8000/courses/4/prerequisites' \
  -H 'X-User-Id: 1' \
  -H 'Content-Type: application/json' \
  -d '{
    "prerequisite_ids": [1, 2]
  }'
```

---

## Modules API

### Create Module

**POST** `/modules/`

**Permissions**: Authenticated users

**Request Body**:
```json
{
  "course_id": 1,
  "name": "Module 1: Python Basics",
  "weight": 1.0
}
```

**Response** (201 Created):
```json
{
  "id": 1,
  "course_id": 1,
  "name": "Module 1: Python Basics",
  "weight": 1.0
}
```

**cURL Example**:
```bash
curl -X 'POST' \
  'http://127.0.0.1:8000/modules/' \
  -H 'X-User-Id: 1' \
  -H 'Content-Type: application/json' \
  -d '{
    "course_id": 1,
    "name": "Module 1: Introduction",
    "weight": 1.0
  }'
```

---

### List Modules by Course

**GET** `/modules/by-course/{course_id}`

**Response** (200 OK):
```json
[
  {
    "id": 1,
    "course_id": 1,
    "name": "Module 1: Python Basics",
    "weight": 1.0
  },
  {
    "id": 2,
    "course_id": 1,
    "name": "Module 2: Data Structures",
    "weight": 1.5
  }
]
```

---

## Lessons API

### Create Lesson

**POST** `/lessons/`

**Permissions**: Authenticated users

**Request Body**:
```json
{
  "module_id": 1,
  "name": "Lesson 1: Variables and Data Types",
  "content_type": "video"
}
```

**Common Content Types**: `video`, `text`, `interactive`, `document`

**Response** (201 Created):
```json
{
  "id": 1,
  "module_id": 1,
  "name": "Lesson 1: Variables and Data Types",
  "content_type": "video"
}
```

**cURL Example**:
```bash
curl -X 'POST' \
  'http://127.0.0.1:8000/lessons/' \
  -H 'X-User-Id: 1' \
  -H 'Content-Type: application/json' \
  -d '{
    "module_id": 1,
    "name": "Lesson 1: Introduction",
    "content_type": "video"
  }'
```

---

### List Lessons by Module

**GET** `/lessons/by-module/{module_id}`

**Response** (200 OK): Array of lesson objects

---

## Assessments API

### Create Assessment

**POST** `/assessments/`

**Permissions**: Admin, Instructor

**Request Body**:
```json
{
  "course_id": 1,
  "type": "exam",
  "total_marks": 100.0
}
```

**Valid Types**: `exam`, `quiz`

**Response** (201 Created):
```json
{
  "id": 1,
  "course_id": 1,
  "type": "exam",
  "total_marks": 100.0
}
```

**cURL Example**:
```bash
curl -X 'POST' \
  'http://127.0.0.1:8000/assessments/' \
  -H 'X-User-Id: 1' \
  -H 'Content-Type: application/json' \
  -d '{
    "course_id": 1,
    "type": "quiz",
    "total_marks": 50.0
  }'
```

---

### Add Question to Assessment

**POST** `/assessments/{assessment_id}/questions`

**Permissions**: Admin, Instructor

**Request Body**:
```json
{
  "content": "What is the time complexity of binary search?",
  "options": [
    {
      "text": "O(n)",
      "is_correct": false
    },
    {
      "text": "O(log n)",
      "is_correct": true
    },
    {
      "text": "O(n log n)",
      "is_correct": false
    },
    {
      "text": "O(1)",
      "is_correct": false
    }
  ]
}
```

**Response** (201 Created):
```json
{
  "id": 1,
  "content": "What is the time complexity of binary search?"
}
```

**cURL Example**:
```bash
curl -X 'POST' \
  'http://127.0.0.1:8000/assessments/1/questions' \
  -H 'X-User-Id: 1' \
  -H 'Content-Type: application/json' \
  -d '{
    "content": "What is Python?",
    "options": [
      {"text": "A programming language", "is_correct": true},
      {"text": "A snake", "is_correct": false}
    ]
  }'
```

---

### List Assessments by Course

**GET** `/assessments/by-course/{course_id}`

**Response** (200 OK): Array of assessment objects

---

## Enrollments API

### Enroll User in Course

**POST** `/enrollments/`

**Permissions**: Authenticated users

**Request Body**:
```json
{
  "user_id": 2,
  "course_id": 1
}
```

**Response** (201 Created):
```json
{
  "id": 1,
  "user_id": 2,
  "course_id": 1,
  "progress": 0.0,
  "completion_percentage": 0.0,
  "last_accessed": null
}
```

**cURL Example**:
```bash
curl -X 'POST' \
  'http://127.0.0.1:8000/enrollments/' \
  -H 'X-User-Id: 1' \
  -H 'Content-Type: application/json' \
  -d '{
    "user_id": 3,
    "course_id": 1
  }'
```

---

### List Enrollments

**GET** `/enrollments/`

**Query Parameters**:
- `offset` (int, default: 0)
- `limit` (int, default: 100)
- `user_id` (int, optional): Filter by user
- `course_id` (int, optional): Filter by course

**Response** (200 OK): Array of enrollment objects

---

### Export Enrollments (CSV Streaming)

**GET** `/enrollments/export`

**Response** (200 OK): CSV file stream

**Headers**:
```
Content-Type: text/csv
Content-Disposition: attachment; filename="enrollments.csv"
```

**cURL Example**:
```bash
curl -X 'GET' \
  'http://127.0.0.1:8000/enrollments/export' \
  -H 'X-User-Id: 1' \
  -o enrollments.csv
```

---

## Submissions API

### Submit Assignment/Assessment

**POST** `/submissions/`

**Permissions**: Authenticated users (learners submit for themselves)

**Request Body**:
```json
{
  "user_id": 2,
  "assessment_id": 1,
  "score": null
}
```

**OR for lesson activity**:
```json
{
  "user_id": 2,
  "lesson_activity_id": 5,
  "score": null
}
```

**Note**: Provide either `assessment_id` OR `lesson_activity_id`, not both.

**Response** (201 Created):
```json
{
  "id": 1,
  "user_id": 2,
  "assessment_id": 1,
  "lesson_activity_id": null,
  "score": null,
  "submitted_at": "2025-12-17T10:30:00Z"
}
```

**cURL Example**:
```bash
curl -X 'POST' \
  'http://127.0.0.1:8000/submissions/' \
  -H 'X-User-Id: 2' \
  -H 'Content-Type: application/json' \
  -d '{
    "user_id": 2,
    "assessment_id": 1,
    "score": null
  }'
```

---

### Grade Submission

**POST** `/submissions/{submission_id}/grade`

**Permissions**: Admin, Instructor

**Request Body**:
```json
{
  "score": 85.5
}
```

**Response** (200 OK):
```json
{
  "id": 1,
  "user_id": 2,
  "assessment_id": 1,
  "lesson_activity_id": null,
  "score": 85.5,
  "submitted_at": "2025-12-17T10:30:00Z"
}
```

**cURL Example**:
```bash
curl -X 'POST' \
  'http://127.0.0.1:8000/submissions/1/grade' \
  -H 'X-User-Id: 1' \
  -H 'Content-Type: application/json' \
  -d '{
    "score": 92.0
  }'
```

---

## Error Responses

### 401 Unauthorized
```json
{
  "detail": "X-User-Id header required"
}
```
or
```json
{
  "detail": "User not found"
}
```

### 403 Forbidden
```json
{
  "detail": "Only admins can perform this action"
}
```

### 404 Not Found
```json
{
  "detail": "Course not found"
}
```

### 422 Validation Error
```json
{
  "detail": [
    {
      "loc": ["body", "email"],
      "msg": "field required",
      "type": "value_error.missing"
    }
  ]
}
```

### 500 Internal Server Error
```json
{
  "detail": "Internal server error"
}
```

---

## Common Workflows

### 1. Complete Course Setup Flow

```bash
# 1. Create instructor user
curl -X POST http://127.0.0.1:8000/users/ \
  -H "X-User-Id: 1" \
  -H "Content-Type: application/json" \
  -d '{"email": "instructor@example.com", "first_name": "Jane", "last_name": "Smith", "role": "instructor"}'

# 2. Create course
curl -X POST http://127.0.0.1:8000/courses/ \
  -H "X-User-Id: 1" \
  -H "Content-Type: application/json" \
  -d '{"title": "Python Basics", "description": "Learn Python", "category": "Programming", "instructor_id": 2}'

# 3. Create module
curl -X POST http://127.0.0.1:8000/modules/ \
  -H "X-User-Id: 1" \
  -H "Content-Type: application/json" \
  -d '{"course_id": 1, "name": "Module 1", "weight": 1.0}'

# 4. Create lesson
curl -X POST http://127.0.0.1:8000/lessons/ \
  -H "X-User-Id: 1" \
  -H "Content-Type: application/json" \
  -d '{"module_id": 1, "name": "Lesson 1", "content_type": "video"}'

# 5. Create assessment
curl -X POST http://127.0.0.1:8000/assessments/ \
  -H "X-User-Id: 1" \
  -H "Content-Type: application/json" \
  -d '{"course_id": 1, "type": "quiz", "total_marks": 100.0}'

# 6. Add question to assessment
curl -X POST http://127.0.0.1:8000/assessments/1/questions \
  -H "X-User-Id: 1" \
  -H "Content-Type: application/json" \
  -d '{"content": "What is Python?", "options": [{"text": "Language", "is_correct": true}]}'
```

### 2. Enrollment and Submission Flow

```bash
# 1. Enroll learner
curl -X POST http://127.0.0.1:8000/enrollments/ \
  -H "X-User-Id: 1" \
  -H "Content-Type: application/json" \
  -d '{"user_id": 3, "course_id": 1}'

# 2. Learner submits assessment
curl -X POST http://127.0.0.1:8000/submissions/ \
  -H "X-User-Id: 3" \
  -H "Content-Type: application/json" \
  -d '{"user_id": 3, "assessment_id": 1, "score": null}'

# 3. Instructor grades submission
curl -X POST http://127.0.0.1:8000/submissions/1/grade \
  -H "X-User-Id: 2" \
  -H "Content-Type: application/json" \
  -d '{"score": 85.0}'
```

---

## Rate Limiting & Best Practices

- **Authentication**: Always include `X-User-Id` header
- **Permissions**: Check role requirements before making requests
- **Pagination**: Use `offset` and `limit` for large datasets
- **Error Handling**: Check status codes and error messages
- **CSV Export**: Use streaming for large exports (100k+ rows)

---

## Swagger UI

For interactive API testing, visit:
- **Swagger UI**: http://127.0.0.1:8000/docs
- **ReDoc**: http://127.0.0.1:8000/redoc
- **OpenAPI JSON**: http://127.0.0.1:8000/openapi.json

---

## Support

For issues or questions, please refer to the main [README.md](./README.md) or open an issue in the repository.

