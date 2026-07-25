from datetime import datetime
from pydantic import BaseModel, EmailStr
from typing import Optional


class SignUpSchema(BaseModel):
    first_name: str
    last_name: str
    email: EmailStr
    password: str


class SignInSchema(BaseModel):
    email: EmailStr
    password: str
    remember: bool = False


class PasswordResetSchema(BaseModel):
    email: EmailStr


class PasswordSetSchema(BaseModel):
    password: str
    # confirm_password: str


class UserSchema(BaseModel):
    id: int
    uuid: str
    first_name: str
    last_name: str
    email: EmailStr
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class SaveRefreshToken(BaseModel):
    user_uuid: str
    token: str
    expires_at: datetime


class RefreshTokenRequest(BaseModel):
    refresh_token: str


class TokenData(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = 'bearer'


class TokenResponseSchema(BaseModel):
    message: str
    action: str
    success: bool
    token: Optional[TokenData] = None
