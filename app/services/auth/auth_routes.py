"""
Authentication routes for user registration and login.
"""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.db.session import get_db_session
from app.schemas.auth import Token, UserLogin, UserRegister
from app.services.auth.auth_service import AuthService

router = APIRouter()


@router.post(
    "/register",
    response_model=Token,
    status_code=status.HTTP_201_CREATED,
    summary="Register a new user",
    tags=["Authentication"],
)
async def register(
    payload: UserRegister,
    session: AsyncSession = Depends(get_db_session),
) -> Token:
    """
    Register a new user account.
    
    Creates a new user with the provided information and returns an access token.
    """
    service = AuthService(session)
    user = await service.register_user(payload)
    token_data = await service.create_token_for_user(user)
    return Token(**token_data)


@router.post(
    "/login",
    response_model=Token,
    summary="Login with email and password",
    tags=["Authentication"],
)
async def login(
    payload: UserLogin,
    session: AsyncSession = Depends(get_db_session),
) -> Token:
    """
    Authenticate a user and return an access token.
    
    Requires valid email and password credentials.
    """
    service = AuthService(session)
    user = await service.authenticate_user(payload)
    token_data = await service.create_token_for_user(user)
    return Token(**token_data)
