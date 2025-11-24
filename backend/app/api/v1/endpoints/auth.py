from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel, EmailStr
from app.db.supabase import get_supabase
from supabase import Client
from app.core.auth import get_current_user
from app.core.logging import get_logger
from app.core.exceptions import AuthenticationError, ValidationError

router = APIRouter()
logger = get_logger(__name__)


class SignupRequest(BaseModel):
    email: EmailStr
    password: str


class LoginRequest(BaseModel):
    email: EmailStr
    password: str


@router.post("/signup", status_code=status.HTTP_201_CREATED)
async def signup(
    request: SignupRequest,
    supabase: Client = Depends(get_supabase)
):
    """
    Sign up a new user.

    Args:
        request: Signup request with email and password
        supabase: Supabase client

    Returns:
        User session data
    """
    try:
        logger.info(f"Signup attempt for email: {request.email}")

        if len(request.password) < 8:
            raise ValidationError("Password must be at least 8 characters long")

        res = supabase.auth.sign_up({
            "email": request.email,
            "password": request.password
        })

        logger.info(f"User signed up successfully: {request.email}")
        return {
            "user": res.user,
            "session": res.session
        }

    except ValidationError:
        raise
    except Exception as e:
        logger.error(f"Signup error for {request.email}: {str(e)}")
        raise AuthenticationError(f"Signup failed: {str(e)}")


@router.post("/login")
async def login(
    request: LoginRequest,
    supabase: Client = Depends(get_supabase)
):
    """
    Log in an existing user.

    Args:
        request: Login request with email and password
        supabase: Supabase client

    Returns:
        User session data with access token
    """
    try:
        logger.info(f"Login attempt for email: {request.email}")

        res = supabase.auth.sign_in_with_password({
            "email": request.email,
            "password": request.password
        })

        logger.info(f"User logged in successfully: {request.email}")
        return {
            "user": res.user,
            "session": res.session,
            "access_token": res.session.access_token if res.session else None
        }

    except Exception as e:
        logger.error(f"Login error for {request.email}: {str(e)}")
        raise AuthenticationError("Invalid email or password")


@router.get("/me")
async def get_me(current_user=Depends(get_current_user)):
    """
    Get current user information.

    Args:
        current_user: Authenticated user from JWT token

    Returns:
        Current user data
    """
    logger.info(f"Fetching user info for user {current_user.id}")
    return {
        "id": current_user.id,
        "email": current_user.email,
        "created_at": current_user.created_at
    }


@router.post("/logout")
async def logout(
    current_user=Depends(get_current_user),
    supabase: Client = Depends(get_supabase)
):
    """
    Log out the current user.

    Args:
        current_user: Authenticated user
        supabase: Supabase client

    Returns:
        Success message
    """
    try:
        logger.info(f"Logout for user {current_user.id}")
        supabase.auth.sign_out()
        return {"message": "Logged out successfully"}
    except Exception as e:
        logger.error(f"Logout error: {str(e)}")
        raise AuthenticationError(f"Logout failed: {str(e)}")
