"""Redis service for token storage and blacklisting"""

import redis.asyncio as redis
from app.config import settings
from typing import Optional
import logging

logger = logging.getLogger(__name__)


class RedisService:
    """Redis service for managing refresh tokens, CSRF tokens, and rate limiting"""

    def __init__(self):
        self.redis: Optional[redis.Redis] = None

    async def connect(self):
        """Initialize Redis connection"""
        try:
            self.redis = await redis.from_url(
                settings.REDIS_URL,
                encoding="utf-8",
                decode_responses=True
            )
            # Test connection
            await self.redis.ping()
            logger.info("Redis connected successfully")
        except Exception as e:
            logger.error(f"Failed to connect to Redis: {e}")
            raise

    async def close(self):
        """Close Redis connection"""
        if self.redis:
            await self.redis.close()
            logger.info("Redis connection closed")

    # Refresh Token Storage (with rotation)
    async def store_refresh_token(self, user_id: str, token_jti: str, expires_in: int):
        """Store refresh token JTI with user_id for revocation tracking"""
        key = f"refresh_token:{user_id}:{token_jti}"
        await self.redis.setex(key, expires_in, "1")
        logger.debug(f"Stored refresh token for user {user_id}")

    async def revoke_refresh_token(self, user_id: str, token_jti: str):
        """Revoke a specific refresh token"""
        key = f"refresh_token:{user_id}:{token_jti}"
        deleted = await self.redis.delete(key)
        if deleted:
            logger.info(f"Revoked refresh token for user {user_id}")
        return deleted > 0

    async def is_refresh_token_valid(self, user_id: str, token_jti: str) -> bool:
        """Check if refresh token is still valid (not revoked)"""
        key = f"refresh_token:{user_id}:{token_jti}"
        exists = await self.redis.exists(key)
        return exists > 0

    async def revoke_all_user_tokens(self, user_id: str):
        """Revoke all refresh tokens for a user (logout all devices)"""
        pattern = f"refresh_token:{user_id}:*"
        count = 0
        async for key in self.redis.scan_iter(match=pattern):
            await self.redis.delete(key)
            count += 1
        logger.info(f"Revoked {count} refresh tokens for user {user_id}")
        return count

    # CSRF Token Storage
    async def store_csrf_token(self, token: str, expires_in: int):
        """Store CSRF token for one-time validation"""
        key = f"csrf:{token}"
        await self.redis.setex(key, expires_in, "1")
        logger.debug("Stored CSRF token")

    async def validate_csrf_token(self, token: str) -> bool:
        """Validate and consume CSRF token (one-time use)"""
        key = f"csrf:{token}"
        exists = await self.redis.exists(key)
        if exists:
            await self.redis.delete(key)  # One-time use - consume it
            logger.debug("CSRF token validated and consumed")
            return True
        logger.warning("Invalid or already used CSRF token")
        return False

    # Rate Limiting
    async def check_rate_limit(self, identifier: str, max_requests: int, window_seconds: int) -> bool:
        """
        Check if request is within rate limit
        Returns True if request is allowed, False if limit exceeded
        """
        key = f"rate_limit:{identifier}"
        current = await self.redis.get(key)

        if current is None:
            # First request in window
            await self.redis.setex(key, window_seconds, "1")
            return True

        current_count = int(current)
        if current_count >= max_requests:
            logger.warning(f"Rate limit exceeded for {identifier}")
            return False

        # Increment counter
        await self.redis.incr(key)
        return True


# Global Redis service instance
redis_service = RedisService()
