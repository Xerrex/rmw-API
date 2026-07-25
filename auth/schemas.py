from datetime import datetime
from pydantic import BaseModel, EmailStr


class SignUpSchema(BaseModel):
    first_name: str
    last_name: str
    email: EmailStr
    password: str


class SignInSchema(BaseModel):
    email: EmailStr
    password: str
    remember: bool


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
