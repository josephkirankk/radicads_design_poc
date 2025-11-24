"""
Custom exceptions and exception handlers for Radic API.
"""

from fastapi import Request, status
from fastapi.responses import JSONResponse
from loguru import logger


class RadicException(Exception):
    """Base exception for Radic application."""
    
    def __init__(
        self,
        message: str,
        status_code: int = status.HTTP_500_INTERNAL_SERVER_ERROR,
        error_code: str = "INTERNAL_ERROR"
    ):
        self.message = message
        self.status_code = status_code
        self.error_code = error_code
        super().__init__(self.message)


class AuthenticationError(RadicException):
    """Raised when authentication fails."""
    
    def __init__(self, message: str = "Authentication failed"):
        super().__init__(
            message=message,
            status_code=status.HTTP_401_UNAUTHORIZED,
            error_code="AUTH_ERROR"
        )


class AuthorizationError(RadicException):
    """Raised when user doesn't have permission."""
    
    def __init__(self, message: str = "Permission denied"):
        super().__init__(
            message=message,
            status_code=status.HTTP_403_FORBIDDEN,
            error_code="PERMISSION_DENIED"
        )


class NotFoundError(RadicException):
    """Raised when resource is not found."""
    
    def __init__(self, message: str = "Resource not found"):
        super().__init__(
            message=message,
            status_code=status.HTTP_404_NOT_FOUND,
            error_code="NOT_FOUND"
        )


class ValidationError(RadicException):
    """Raised when input validation fails."""
    
    def __init__(self, message: str = "Validation failed"):
        super().__init__(
            message=message,
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            error_code="VALIDATION_ERROR"
        )


class AIServiceError(RadicException):
    """Raised when AI service fails."""
    
    def __init__(self, message: str = "AI service error"):
        super().__init__(
            message=message,
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            error_code="AI_SERVICE_ERROR"
        )


class DatabaseError(RadicException):
    """Raised when database operation fails."""
    
    def __init__(self, message: str = "Database error"):
        super().__init__(
            message=message,
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            error_code="DATABASE_ERROR"
        )


async def radic_exception_handler(request: Request, exc: RadicException):
    """
    Handle RadicException and return structured JSON response.
    
    Args:
        request: FastAPI request object
        exc: RadicException instance
        
    Returns:
        JSONResponse with error details
    """
    logger.error(
        f"RadicException: {exc.error_code} - {exc.message} | "
        f"Path: {request.url.path} | Method: {request.method}"
    )
    
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "error": exc.error_code,
            "message": exc.message,
            "path": str(request.url.path)
        }
    )


async def general_exception_handler(request: Request, exc: Exception):
    """
    Handle unexpected exceptions and return generic error response.
    
    Args:
        request: FastAPI request object
        exc: Exception instance
        
    Returns:
        JSONResponse with generic error message
    """
    logger.exception(
        f"Unhandled exception: {type(exc).__name__} - {str(exc)} | "
        f"Path: {request.url.path} | Method: {request.method}"
    )
    
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={
            "error": "INTERNAL_ERROR",
            "message": "An unexpected error occurred. Please try again later.",
            "path": str(request.url.path)
        }
    )

