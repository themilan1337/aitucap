from typing import Optional
from fastapi import Depends, HTTPException, status, Cookie
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db
from app.services.auth_service import auth_service
from app.models.user import User
from sqlalchemy import select
import logging

logger = logging.getLogger(__name__)


async def get_current_user(
    db: AsyncSession = Depends(get_db),
    access_token: Optional[str] = Cookie(None)  # Read from HttpOnly cookie
) -> User:
    """
    Dependency to get current authenticated user from HttpOnly cookie
    """
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    if not access_token:
        logger.debug("No access token found in cookies")
        raise credentials_exception

    # Decode and validate JWT
    payload = auth_service.decode_token(access_token)
    if not payload or payload.get("type") != "access":
        logger.warning("Invalid access token")
        raise credentials_exception

    user_id: str = payload.get("sub")
    if user_id is None:
        raise credentials_exception

    # Get user from database
    result = await db.execute(select(User).filter(User.id == user_id))
    user = result.scalars().first()

    if user is None:
        logger.warning(f"User not found for ID: {user_id}")
        raise credentials_exception

    return user


async def get_optional_user(
    db: AsyncSession = Depends(get_db),
    access_token: Optional[str] = Cookie(None)
) -> Optional[User]:
    """
    Optional authentication - returns None if not authenticated
    Useful for endpoints that work both with and without authentication
    """
    if not access_token:
        return None

    try:
        return await get_current_user(db, access_token)
    except HTTPException:
        return None
