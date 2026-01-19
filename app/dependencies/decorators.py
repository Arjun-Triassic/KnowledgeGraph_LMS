"""
Custom decorators and dependencies for FastAPI.
Includes CSV validation, payload preprocessing, and role-based access control.
"""
from __future__ import annotations

import csv
import io
from functools import wraps
from typing import Any, Callable, List, Optional, Type

from fastapi import Depends, HTTPException, Request, UploadFile, status
from pydantic import BaseModel

from app.core.models.enums import UserRole
from app.core.models.user import User
from app.dependencies.auth import get_current_user


def validate_csv_headers(required_headers: List[str]):
    """
    Dependency factory that validates CSV file headers.
    
    Usage:
        @router.post("/upload")
        async def upload_csv(
            file: UploadFile = Depends(validate_csv_headers(["user_id", "course_id", "progress"]))
        ):
            ...
    """
    
    async def dependency(file: UploadFile) -> UploadFile:
        # Read first line to validate headers
        content = await file.read()
        file.file.seek(0)  # Reset file pointer
        
        # Decode and parse CSV
        try:
            text_content = content.decode("utf-8")
            reader = csv.reader(io.StringIO(text_content))
            headers = next(reader, None)
            
            if not headers:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="CSV file is empty or has no headers",
                )
            
            # Normalize headers (strip whitespace, lowercase)
            normalized_headers = [h.strip().lower() for h in headers]
            normalized_required = [h.strip().lower() for h in required_headers]
            
            # Check if all required headers are present
            missing_headers = set(normalized_required) - set(normalized_headers)
            if missing_headers:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=f"Missing required CSV headers: {', '.join(missing_headers)}",
                )
        except UnicodeDecodeError:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="CSV file must be UTF-8 encoded",
            )
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Error reading CSV file: {str(e)}",
            )
        
        return file
    
    return dependency


def preprocess_payload(model_class: Type[BaseModel]):
    """
    Dependency that preprocesses request payload by cleaning strings and trimming whitespace.
    
    Usage:
        @router.post("/")
        async def create_item(
            payload: ItemCreate = Depends(preprocess_payload(ItemCreate))
        ):
            ...
    """
    
    async def dependency(request: Request) -> BaseModel:
        body = await request.json()
        
        # Recursively clean string values
        def clean_value(value: Any) -> Any:
            if isinstance(value, str):
                return value.strip()
            elif isinstance(value, dict):
                return {k: clean_value(v) for k, v in value.items()}
            elif isinstance(value, list):
                return [clean_value(item) for item in value]
            return value
        
        cleaned_body = clean_value(body)
        return model_class(**cleaned_body)
    
    return dependency


def role_required(allowed_roles: List[UserRole]):
    """
    Dependency factory for role-based access control.
    More convenient than get_permission_checker for simple role checks.
    
    Usage:
        @router.post("/")
        async def create_course(
            current_user: User = Depends(role_required([UserRole.ADMIN, UserRole.INSTRUCTOR]))
        ):
            ...
    """
    
    async def dependency(user: User = Depends(get_current_user)) -> User:
        if user.role not in allowed_roles:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"Access denied. Required roles: {[r.value for r in allowed_roles]}",
            )
        return user
    
    return dependency


def log_api_usage(endpoint_name: Optional[str] = None):
    """
    Decorator that logs API usage metrics.
    Note: The AuditMiddleware already logs all requests, but this decorator
    can be used for additional custom logging if needed.
    
    Usage:
        @router.post("/")
        @log_api_usage("create_user")
        async def create_user(...):
            ...
    """
    def decorator(func: Callable) -> Callable:
        @wraps(func)
        async def wrapper(*args, **kwargs):
            # The AuditMiddleware already handles logging
            # This decorator is here for extensibility
            # You can add custom logging logic here if needed
            return await func(*args, **kwargs)
        return wrapper
    return decorator
