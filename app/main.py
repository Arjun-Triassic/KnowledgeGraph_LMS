from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware 
from app.middleware.audit import AuditMiddleware
from app.services.auth.auth_routes import router as auth_router
from app.services.users.user_routes import router as users_router
from app.services.courses.course_routes import router as courses_router
from app.services.modules.module_routes import router as modules_router
from app.services.lessons.lesson_routes import router as lessons_router
from app.services.assessments.assessment_routes import router as assessments_router
from app.services.enrollments.enrollment_routes import router as enrollments_router
from app.services.submissions.submission_routes import router as submissions_router


def create_app() -> FastAPI:
    """
    Application factory for the KnowledgeGraph LMS backend.
    """

    app = FastAPI(
        title="KnowledgeGraph LMS",
        description="Async FastAPI backend for a complex LMS with courses, modules, lessons, "
        "assessments, enrollments, and submissions.",
        version="1.0.0",
    )

    
    # Routers
    app.include_router(auth_router, prefix="/auth", tags=["Authentication"])
    app.include_router(users_router, prefix="/users", tags=["Users"])
    app.include_router(courses_router, prefix="/courses", tags=["Courses"])
    app.include_router(modules_router, prefix="/modules", tags=["Modules"])
    app.include_router(lessons_router, prefix="/lessons", tags=["Lessons"])
    app.include_router(assessments_router, prefix="/assessments", tags=["Assessments"])
    app.include_router(enrollments_router, prefix="/enrollments", tags=["Enrollments"])
    app.include_router(submissions_router, prefix="/submissions", tags=["Submissions"])

    # Middleware
    app.add_middleware(AuditMiddleware)

    return app


app = create_app()


