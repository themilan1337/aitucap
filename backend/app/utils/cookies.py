"""Cookie management utilities"""

from fastapi import Response
from app.config import settings


def set_auth_cookies(response: Response, access_token: str, refresh_token: str, remember_me: bool = False):
    """Set HttpOnly authentication cookies with proper security flags"""

    # Determine Max-Age for refresh token based on remember_me
    refresh_max_age = settings.COOKIE_MAX_AGE_REMEMBER if remember_me else settings.COOKIE_MAX_AGE_STANDARD

    # Access token cookie (short-lived, 30 min)
    response.set_cookie(
        key="access_token",
        value=access_token,
        httponly=True,  # JavaScript cannot access (XSS protection)
        secure=settings.COOKIE_SECURE,  # True in production (HTTPS only)
        samesite=settings.COOKIE_SAMESITE,  # "lax" for CSRF protection
        max_age=settings.ACCESS_TOKEN_EXPIRE_MINUTES * 60,
        path="/",  # Available on all paths
        domain=settings.COOKIE_DOMAIN if settings.is_production else None
    )

    # Refresh token cookie (long-lived, 7 or 30 days)
    response.set_cookie(
        key="refresh_token",
        value=refresh_token,
        httponly=True,
        secure=settings.COOKIE_SECURE,
        samesite=settings.COOKIE_SAMESITE,
        max_age=refresh_max_age,
        path="/api/v1/auth/refresh",  # Restricted path for security
        domain=settings.COOKIE_DOMAIN if settings.is_production else None
    )


def clear_auth_cookies(response: Response):
    """Clear authentication cookies on logout"""
    response.delete_cookie(
        key="access_token",
        path="/",
        domain=settings.COOKIE_DOMAIN if settings.is_production else None
    )
    response.delete_cookie(
        key="refresh_token",
        path="/api/v1/auth/refresh",
        domain=settings.COOKIE_DOMAIN if settings.is_production else None
    )
