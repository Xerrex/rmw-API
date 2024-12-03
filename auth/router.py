from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from db.db_deps import get_db
from .schemas import SignUpSchema, SignInSchema
from .crud import create_user, get_user_by_email



router = APIRouter()


@router.post("/signup")
def signUp(signUpData: SignUpSchema, db:Session = Depends(get_db)):
    """Sign Up: 
    create a new user account.
    """

    user = get_user_by_email(email=signUpData.email, db=db)

    if user:
        detail = f"User with email {signUpData.email} exists"
        raise HTTPException(status_code=409, detail=detail)

    new_user = create_user(userData=signUpData, db=db)
    if new_user:
        return {
            "message": "Successful sign up",
            "details": {
                "first_name": new_user.first_name,
                "last_name": new_user.last_name,
                "email": new_user.email
            }
        }
    


@router.post("/signin")
def signIn():
    """Sign in
    Assigns an already signed up user a auth token for session  management.
    """
    return {
        "message": "sign in"
    }


@router.post("/reset-password")
def reset_password():
    return {
        "message": "reset password"
    }


@router.put("/set-password")
def set_password():
    return {
        "message": "set password"
    }