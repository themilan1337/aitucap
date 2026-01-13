"""CSRF protection utilities"""

from fastapi import Header, HTTPException, status, Response
from app.services.auth_service import auth_service
from app.services.redis_service import redis_service
from app.config import settings
import logging

logger = logging.getLogger(__name__)


async def get_csrf_token(x_csrf_token: str = Header(...)) -> str:
    """
    Validate CSRF token from header
    Used as dependency for state-changing operations
    """
    # Validate token format
    if not auth_service.validate_csrf_token(x_csrf_token):
        logger.warning("Invalid CSRF token format")
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Invalid CSRF token"
        )

    # Check if token exists in Redis (prevents replay attacks)
    if not await redis_service.validate_csrf_token(x_csrf_token):
        logger.warning("CSRF token expired or already used")
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="CSRF token expired or already used"
        )

    return x_csrf_token


async def generate_csrf_response(response: Response) -> str:
    """
    Generate CSRF token and set it in response header
    Returns the token so it can be sent in response body too
    """
    csrf_token = auth_service.create_csrf_token()

    # Store in Redis with TTL
    await redis_service.store_csrf_token(
        csrf_token,
        expires_in=settings.CSRF_TOKEN_EXPIRE_MINUTES * 60
    )

    # Set in response header for client to store
    response.headers["X-CSRF-Token"] = csrf_token

    logger.debug("Generated CSRF token")
    return csrf_token
