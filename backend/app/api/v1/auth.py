from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.database import get_db
from app.api.deps import get_current_user
from app.schemas.auth import Token, OAuthLoginRequest, UserResponse
from app.services.auth_service import auth_service
from app.models.user import User, UserProfile
import logging

logger = logging.getLogger(__name__)
router = APIRouter()

@router.post("/login/oauth", response_model=Token)
async def oauth_login(
    request: OAuthLoginRequest,
    db: AsyncSession = Depends(get_db)
):
    """Login or Register with Google OAuth"""

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
    
    if not user:
        # Register new user
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
        
    # Generate tokens
    access_token = auth_service.create_access_token(data={"sub": str(user.id)})
    refresh_token = auth_service.create_refresh_token(data={"sub": str(user.id)})
    
    return {
        "access_token": access_token,
        "refresh_token": refresh_token,
        "token_type": "bearer"
    }

@router.post("/refresh", response_model=Token)
async def refresh_token(
    refresh_token: str,
    db: AsyncSession = Depends(get_db)
):
    """Refresh access token"""
    payload = auth_service.decode_token(refresh_token)
    if not payload or payload.get("type") != "refresh":
        raise HTTPException(status_code=401, detail="Invalid refresh token")
        
    user_id = payload.get("sub")
    if not user_id:
        raise HTTPException(status_code=401, detail="Invalid refresh token")
        
    # Optional: check if user still exists/active
    
    new_access_token = auth_service.create_access_token(data={"sub": user_id})
    new_refresh_token = auth_service.create_refresh_token(data={"sub": user_id})
    
    return {
        "access_token": new_access_token,
        "refresh_token": new_refresh_token,
        "token_type": "bearer"
    }

@router.get("/me", response_model=UserResponse)
async def get_me(current_user: User = Depends(get_current_user)):
    """Get current user info"""
    return current_user
