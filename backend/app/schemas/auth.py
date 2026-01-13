"""Authentication schemas"""

from pydantic import BaseModel, EmailStr
from typing import Optional


class OAuthLoginRequest(BaseModel):
    """OAuth login request with CSRF protection and Remember Me"""
    id_token: str
    provider: str  # 'google'
    csrf_token: str  # CSRF protection
    remember_me: bool = False  # 30-day refresh token if True


class CSRFTokenResponse(BaseModel):
    """CSRF token response"""
    csrf_token: str


class LogoutResponse(BaseModel):
    """Logout response"""
    message: str


class UserResponse(BaseModel):
    """User data response (NO tokens in body - they're in HttpOnly cookies)"""
    id: str
    email: EmailStr
    full_name: Optional[str]
    avatar_url: Optional[str]
    oauth_provider: str

    class Config:
        from_attributes = True
