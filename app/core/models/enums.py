from enum import Enum


class UserRole(str, Enum):
    ADMIN = "admin"
    INSTRUCTOR = "instructor"
    LEARNER = "learner"


class LessonActivityType(str, Enum):
    QUIZ = "quiz"
    ASSIGNMENT = "assignment"
    PROJECT = "project"


class AssessmentType(str, Enum):
    EXAM = "exam"
    QUIZ = "quiz"


class AuditEventType(str, Enum):
    REQUEST = "request"
    ERROR = "error"



