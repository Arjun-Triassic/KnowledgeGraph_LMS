# KnowledgeGraph LMS

A comprehensive Learning Management System (LMS) backend built with FastAPI, featuring complex relational structures, async processing, streaming responses, CSV ingestion, and automated workflows.

## 🚀 Features

- **Async FastAPI** with SQLAlchemy 2.0 async ORM
- **Complex relational data structures** with many-to-many relationships
- **Role-based access control** (Admin, Instructor, Learner)
- **CSV import/export** with streaming support
- **Audit logging** middleware for all requests
- **Course prerequisites** (self-referential many-to-many)
- **Assessment and submission** management
- **Enrollment tracking** with progress monitoring
- **Swagger/OpenAPI** documentation

## 📋 Prerequisites

- Python 3.10+
- PostgreSQL 12+
- pip (Python package manager)

## 🛠️ Installation

### 1. Clone the Repository

```bash
git clone <repository-url>
cd KnowledgeGraph_LMS
```

### 2. Create Virtual Environment

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Database Setup

#### Option A: Using PostgreSQL CLI

```bash
# Switch to postgres user
sudo -i -u postgres

# Enter PostgreSQL shell
psql

# Create database and user
CREATE DATABASE knowledgegraph_lms;
CREATE USER kg_user WITH PASSWORD 'kg_password';
GRANT ALL PRIVILEGES ON DATABASE knowledgegraph_lms TO kg_user;
ALTER USER kg_user CREATEDB;

# Exit psql
\q
exit
```

#### Option B: Using SQL Script

```bash
psql -U postgres -f setup_database.sql
```

### 5. Environment Configuration

Create a `.env` file in the project root:

```env
DATABASE_URL=postgresql+asyncpg://kg_user:kg_password@localhost:5432/knowledgegraph_lms
```

**Note:** Adjust the connection string if your PostgreSQL setup differs.

### 6. Run Database Migrations

```bash
# From project root
alembic -c alembic.ini upgrade head
```

### 7. Bootstrap Admin User

Create the first admin user:

```bash
python bootstrap_admin.py
```

This will create an admin user and display the user ID. **Save this ID** - you'll need it for API authentication.

## 🏃 Running the Application

### Development Server

```bash
# From project root
uvicorn app.main:app --reload
```

The API will be available at:
- **API**: http://127.0.0.1:8000
- **Swagger UI**: http://127.0.0.1:8000/docs
- **ReDoc**: http://127.0.0.1:8000/redoc

### Production Server

```bash
uvicorn app.main:app --host 0.0.0.0 --port 8000
```

## 📚 Project Structure

```
app/
├── main.py                 # FastAPI application entry point
├── core/
│   ├── config.py          # Application configuration
│   ├── db/                # Database setup (async engine, session)
│   ├── models/            # SQLAlchemy ORM models
│   └── common/            # Base service class
├── schemas/               # Pydantic request/response schemas
├── services/              # Business logic and API routes
│   ├── users/
│   ├── courses/
│   ├── modules/
│   ├── lessons/
│   ├── assessments/
│   ├── enrollments/
│   └── submissions/
├── dependencies/          # Auth and permission dependencies
├── middleware/            # Audit logging middleware
└── alembic/              # Database migrations
```

## 🔐 Authentication

The API uses a simple header-based authentication system:

- **Header**: `X-User-Id: <user_id>`
- **Required**: For all protected endpoints
- **User ID**: Must exist in the database

**Example:**
```bash
curl -H "X-User-Id: 1" http://127.0.0.1:8000/users/
```

## 👥 User Roles

- **Admin**: Full system access
- **Instructor**: Can create/manage courses, assessments, grade submissions
- **Learner**: Can enroll in courses, submit assignments/assessments

## 🧪 Testing

### Quick Test Script

```bash
# Make sure server is running first
./test_api.sh
```

### Manual Testing

1. Open Swagger UI: http://127.0.0.1:8000/docs
2. Use the `X-User-Id` from bootstrap (usually `1`)
3. Test endpoints interactively

## 📖 API Documentation

See [API_DOCUMENTATION.md](./API_DOCUMENTATION.md) for complete API reference with all endpoints, payloads, and examples.

## 🔧 Database Migrations

### Create a new migration

```bash
alembic -c alembic.ini revision --autogenerate -m "description"
```

### Apply migrations

```bash
alembic -c alembic.ini upgrade head
```

### Rollback migration

```bash
alembic -c alembic.ini downgrade -1
```

## 🐛 Troubleshooting

### Database Connection Issues

- Verify PostgreSQL is running: `sudo systemctl status postgresql`
- Check `.env` file has correct `DATABASE_URL`
- Ensure database and user exist
- Test connection: `psql -U kg_user -d knowledgegraph_lms`

### Migration Issues

- Ensure database exists before running migrations
- Check `alembic.ini` has correct script location
- Verify all models are imported in `alembic/env.py`

### Authentication Errors

- Ensure admin user exists (run `bootstrap_admin.py`)
- Verify `X-User-Id` header matches existing user ID
- Check user role has required permissions

### Import Errors

- Activate virtual environment: `source venv/bin/activate`
- Reinstall dependencies: `pip install -r requirements.txt`
- Ensure you're running from project root

## 📝 Environment Variables

| Variable | Description | Example |
|----------|-------------|---------|
| `DATABASE_URL` | Async PostgreSQL connection string | `postgresql+asyncpg://user:pass@localhost:5432/dbname` |
| `ALEMBIC_DATABASE_URL` | Optional sync DB URL for Alembic | `postgresql+psycopg2://user:pass@localhost:5432/dbname` |

## 🏗️ Architecture

- **Framework**: FastAPI (async)
- **ORM**: SQLAlchemy 2.0 (async)
- **Database**: PostgreSQL with asyncpg driver
- **Validation**: Pydantic v1
- **Migrations**: Alembic
- **API Docs**: Swagger/OpenAPI (auto-generated)

## 📄 License

[Add your license here]

## 👤 Author

[Add your name/contact here]

## 🙏 Acknowledgments

Built with FastAPI, SQLAlchemy, and PostgreSQL.

