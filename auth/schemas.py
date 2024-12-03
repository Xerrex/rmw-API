from pydantic import BaseModel, EmailStr


class SignUpSchema(BaseModel):
    first_name: str
    last_name: str
    email: EmailStr
    password: str


class SignInSchema(BaseModel):
    email: EmailStr
    password: str


class PasswordResetSchema(BaseModel):
    email: EmailStr


class PasswordSetSchema(BaseModel):
    password: str
    confirm_password: str

