from pydantic import BaseModel, EmailStr
from typing import Optional

class Token(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"

class OAuthLoginRequest(BaseModel):
    id_token: str
    provider: str # 'google'

class UserResponse(BaseModel):
    id: str
    email: EmailStr
    full_name: Optional[str]
    avatar_url: Optional[str]
    oauth_provider: str

    class Config:
        from_attributes = True
