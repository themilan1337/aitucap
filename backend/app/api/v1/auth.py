"""Authentication endpoints with cookie-based auth and CSRF protection"""

from fastapi import APIRouter, Depends, HTTPException, status, Response, Cookie
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from typing import Optional

from app.database import get_db
from app.api.deps import get_current_user
from app.api.csrf import generate_csrf_response
from app.schemas.auth import (
    OAuthLoginRequest,
    UserResponse,
    CSRFTokenResponse,
    LogoutResponse
)
from app.services.auth_service import auth_service
from app.services.redis_service import redis_service
from app.utils.cookies import set_auth_cookies, clear_auth_cookies
from app.models.user import User, UserProfile
import logging

logger = logging.getLogger(__name__)
router = APIRouter()


@router.get("/csrf-token", response_model=CSRFTokenResponse)
async def get_csrf_token_endpoint(response: Response):
    """
    Get a CSRF token for state-changing operations
    Frontend must call this before login/logout
    """
    csrf_token = await generate_csrf_response(response)
    return {"csrf_token": csrf_token}


@router.post("/login/oauth", response_model=UserResponse)
async def oauth_login(
    request: OAuthLoginRequest,
    response: Response,
    db: AsyncSession = Depends(get_db)
):
    """
    Login or Register with Google OAuth
    Sets HttpOnly cookies for access and refresh tokens
    Returns user data
    """
    # Verify Google token
    user_info = None
    if request.provider == "google":
        user_info = await auth_service.verify_google_token(request.id_token)
    else:
        raise HTTPException(status_code=400, detail="Invalid provider")

    if not user_info:
        raise HTTPException(status_code=401, detail="Invalid OAuth token")

    # Check if user exists
    result = await db.execute(
        select(User).filter(User.oauth_id == user_info["oauth_id"])
    )
    user = result.scalars().first()

    # Register new user if doesn't exist
    if not user:
        user = User(
            email=user_info["email"],
            full_name=user_info["full_name"],
            avatar_url=user_info["avatar_url"],
            oauth_provider=request.provider,
            oauth_id=user_info["oauth_id"]
        )
        db.add(user)
        await db.commit()
        await db.refresh(user)

        # Create empty profile
        profile = UserProfile(user_id=user.id)
        db.add(profile)
        await db.commit()
        logger.info(f"New user registered: {user.email}")

    # Generate tokens with JTI for refresh token
    access_token = auth_service.create_access_token(data={"sub": str(user.id)})
    refresh_token, refresh_jti, refresh_expires = auth_service.create_refresh_token(
        data={"sub": str(user.id)},
        remember_me=request.remember_me
    )

    # Store refresh token in Redis
    await redis_service.store_refresh_token(
        user_id=str(user.id),
        token_jti=refresh_jti,
        expires_in=refresh_expires
    )

    # Set HttpOnly cookies
    set_auth_cookies(response, access_token, refresh_token, request.remember_me)

    logger.info(f"User logged in: {user.email}, remember_me={request.remember_me}")

    # Return user data (NOT tokens)
    return user


@router.post("/refresh", response_model=UserResponse)
async def refresh_token(
    response: Response,
    db: AsyncSession = Depends(get_db),
    refresh_token: Optional[str] = Cookie(None)
):
    """
    Refresh access token using refresh token from cookie
    Implements token rotation: old refresh token is revoked, new one issued
    """
    if not refresh_token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Refresh token not found"
        )

    # Decode and validate refresh token
    payload = auth_service.decode_token(refresh_token)
    if not payload or payload.get("type") != "refresh":
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid refresh token"
        )

    user_id = payload.get("sub")
    token_jti = payload.get("jti")

    if not user_id or not token_jti:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid refresh token"
        )

    # Check if token is revoked in Redis
    if not await redis_service.is_refresh_token_valid(user_id, token_jti):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Refresh token has been revoked"
        )

    # Verify user still exists
    result = await db.execute(select(User).filter(User.id == user_id))
    user = result.scalars().first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not found"
        )

    # Revoke old refresh token (rotation)
    await redis_service.revoke_refresh_token(user_id, token_jti)

    # Determine if this was a remember_me token (check expiry time)
    # If token had long expiry, keep it
    token_exp = payload.get("exp")
    token_iat = payload.get("iat")
    remember_me = False
    if token_exp and token_iat:
        token_lifetime_days = (token_exp - token_iat) / (24 * 60 * 60)
        remember_me = token_lifetime_days > 10  # More than 10 days means remember_me

    # Generate new tokens
    new_access_token = auth_service.create_access_token(data={"sub": user_id})
    new_refresh_token, new_refresh_jti, refresh_expires = auth_service.create_refresh_token(
        data={"sub": user_id},
        remember_me=remember_me
    )

    # Store new refresh token in Redis
    await redis_service.store_refresh_token(
        user_id=user_id,
        token_jti=new_refresh_jti,
        expires_in=refresh_expires
    )

    # Set new cookies
    set_auth_cookies(response, new_access_token, new_refresh_token, remember_me)

    logger.info(f"Token refreshed for user: {user_id}")

    return user


@router.post("/logout", response_model=LogoutResponse)
async def logout(
    response: Response,
    current_user: User = Depends(get_current_user),
    refresh_token: Optional[str] = Cookie(None)
):
    """
    Logout user (single device)
    Revokes current refresh token and clears cookies
    """
    # Decode refresh token to get JTI
    if refresh_token:
        payload = auth_service.decode_token(refresh_token)
        if payload and payload.get("jti"):
            # Revoke this specific refresh token
            await redis_service.revoke_refresh_token(
                str(current_user.id),
                payload.get("jti")
            )

    # Clear cookies
    clear_auth_cookies(response)

    logger.info(f"User logged out: {current_user.email}")

    return {"message": "Logged out successfully"}


@router.post("/logout-all", response_model=LogoutResponse)
async def logout_all_devices(
    response: Response,
    current_user: User = Depends(get_current_user)
):
    """
    Logout from all devices
    Revokes all refresh tokens for the user
    """
    # Revoke all refresh tokens
    count = await redis_service.revoke_all_user_tokens(str(current_user.id))

    # Clear cookies on this device
    clear_auth_cookies(response)

    logger.info(f"User logged out from all devices ({count} tokens revoked): {current_user.email}")

    return {"message": f"Logged out from all devices ({count} sessions)"}


@router.get("/me", response_model=UserResponse)
async def get_me(current_user: User = Depends(get_current_user)):
    """Get current user info"""
    return current_user
