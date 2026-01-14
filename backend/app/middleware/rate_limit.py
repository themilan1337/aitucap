"""Rate limiting middleware"""

from fastapi import Request, HTTPException, status
from app.services.redis_service import redis_service
from app.config import settings
import logging

logger = logging.getLogger(__name__)


async def rate_limit_middleware(request: Request):
    """
    Rate limiting for authentication endpoints
    Applies per-IP address to prevent brute force attacks
    """
    # Only apply to auth endpoints
    if not request.url.path.startswith("/api/v1/auth"):
        return

    # Get client IP (handle proxied requests)
    client_ip = request.client.host if request.client else "unknown"

    # Also check X-Forwarded-For header for proxied requests
    if "x-forwarded-for" in request.headers:
        client_ip = request.headers["x-forwarded-for"].split(",")[0].strip()

    # Check rate limit in Redis
    # 10 requests per second = 100 requests per 10 seconds
    allowed = await redis_service.check_rate_limit(
        f"auth:{client_ip}",
        max_requests=100,
        window_seconds=10
    )

    if not allowed:
        logger.warning(f"Rate limit exceeded for IP: {client_ip} on path: {request.url.path}")
        raise HTTPException(
            status_code=status.HTTP_429_TOO_MANY_REQUESTS,
            detail="Too many authentication attempts. Please try again later."
        )
