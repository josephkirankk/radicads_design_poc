"""
Authentication middleware for Radic API.
Handles JWT validation and user context extraction from Supabase.
"""

from typing import Optional
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from supabase import Client
from app.db.supabase import get_supabase

security = HTTPBearer()


async def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    supabase: Client = Depends(get_supabase)
):
    """
    Validate JWT token and return current user.
    
    Args:
        credentials: Bearer token from Authorization header
        supabase: Supabase client instance
        
    Returns:
        User object from Supabase auth
        
    Raises:
        HTTPException: If token is invalid or user not found
    """
    try:
        # Get user from Supabase using the JWT token
        user_response = supabase.auth.get_user(credentials.credentials)
        
        if not user_response or not user_response.user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid authentication credentials",
                headers={"WWW-Authenticate": "Bearer"},
            )
        
        return user_response.user
        
    except Exception as e:
        # Log the error (will be implemented with logging system)
        print(f"Authentication error: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )


async def get_current_user_optional(
    credentials: Optional[HTTPAuthorizationCredentials] = Depends(HTTPBearer(auto_error=False)),
    supabase: Client = Depends(get_supabase)
):
    """
    Optional authentication - returns user if token provided, None otherwise.
    Useful for endpoints that work differently for authenticated vs anonymous users.
    
    Args:
        credentials: Optional bearer token from Authorization header
        supabase: Supabase client instance
        
    Returns:
        User object if authenticated, None otherwise
    """
    if not credentials:
        return None
    
    try:
        user_response = supabase.auth.get_user(credentials.credentials)
        if user_response and user_response.user:
            return user_response.user
    except Exception:
        pass
    
    return None


def get_user_id(user) -> str:
    """
    Extract user ID from Supabase user object.
    
    Args:
        user: Supabase user object
        
    Returns:
        User ID string
    """
    return user.id

