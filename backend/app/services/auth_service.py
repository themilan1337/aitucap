import uuid
from datetime import datetime, timedelta
from typing import Optional, Dict, Any, Tuple
from jose import JWTError, jwt
from itsdangerous import URLSafeTimedSerializer
from app.config import settings
import httpx
from google.oauth2 import id_token
from google.auth.transport import requests as google_requests
import logging

logger = logging.getLogger(__name__)


class AuthService:
    """Service for handling authentication and tokens"""

    def __init__(self):
        self.csrf_serializer = URLSafeTimedSerializer(settings.CSRF_SECRET_KEY)

    @staticmethod
    def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
        """Create a new JWT access token (NO JTI - short-lived, stateless)"""
        to_encode = data.copy()
        if expires_delta:
            expire = datetime.utcnow() + expires_delta
        else:
            expire = datetime.utcnow() + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)

        to_encode.update({
            "exp": expire,
            "type": "access",
            "iat": datetime.utcnow()
        })
        return jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)

    @staticmethod
    def create_refresh_token(data: dict, remember_me: bool = False) -> Tuple[str, str, int]:
        """
        Create a new JWT refresh token with JTI for tracking
        Returns: (token, jti, expires_in_seconds)
        """
        to_encode = data.copy()
        jti = str(uuid.uuid4())  # Unique token ID for revocation tracking

        # Determine expiry based on remember_me
        if remember_me:
            days = settings.REFRESH_TOKEN_EXPIRE_DAYS_REMEMBER
        else:
            days = settings.REFRESH_TOKEN_EXPIRE_DAYS

        expires_in_seconds = days * 24 * 60 * 60
        expire = datetime.utcnow() + timedelta(days=days)

        to_encode.update({
            "exp": expire,
            "type": "refresh",
            "jti": jti,
            "iat": datetime.utcnow()
        })

        token = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
        return token, jti, expires_in_seconds

    @staticmethod
    def decode_token(token: str) -> Optional[Dict[str, Any]]:
        """Decode and verify a JWT token"""
        try:
            payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
            return payload
        except JWTError as e:
            logger.warning(f"Token decode failed: {e}")
            return None

    def create_csrf_token(self) -> str:
        """Generate a CSRF token"""
        return self.csrf_serializer.dumps(str(uuid.uuid4()))

    def validate_csrf_token(self, token: str, max_age: int = None) -> bool:
        """Validate CSRF token format (actual validation happens in Redis)"""
        try:
            max_age = max_age or settings.CSRF_TOKEN_EXPIRE_MINUTES * 60
            self.csrf_serializer.loads(token, max_age=max_age)
            return True
        except Exception as e:
            logger.warning(f"CSRF token format validation failed: {e}")
            return False

    @staticmethod
    async def verify_google_token(token: str) -> Optional[Dict[str, Any]]:
        """Verify Google ID token"""
        try:
            # Replaced with google-auth library for better verification
            idinfo = id_token.verify_oauth2_token(
                token, 
                google_requests.Request(), 
                settings.GOOGLE_CLIENT_ID
            )

            if idinfo['iss'] not in ['accounts.google.com', 'https://accounts.google.com']:
                raise ValueError('Wrong issuer.')

            return {
                "oauth_id": idinfo['sub'],
                "email": idinfo.get('email'),
                "full_name": idinfo.get('name'),
                "avatar_url": idinfo.get('picture')
            }
        except Exception as e:
            logger.error(f"Google token verification failed: {e}")
            return None

auth_service = AuthService()
