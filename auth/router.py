from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from db.db_deps import get_db
from .schemas import SignUpSchema, SignInSchema, PasswordResetSchema, PasswordSetSchema
from .crud import create_user, get_user_by_email
from .security import verify_password



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
def signIn(signInData: SignInSchema, db:Session = Depends(get_db)):
    """Sign in
    Assigns an already signed up user a auth token for session  management.
    """
    user = get_user_by_email(email=signInData.email, db=db)

    if not user:
        detail = f"User with email {signInData.email} does not exists"
        raise HTTPException(status_code=404, detail=detail)
    
    if verify_password(signInData.password, user.password):
        
        return {
            "message": "Successful sign in",
            "details": {
                "uuid": user.uuid,
                "first_name": user.first_name,
                "last_name": user.last_name,
                "email": user.email
            }
        }


@router.post("/reset-password")
def reset_password(resetData: PasswordResetSchema, db:Session = Depends(get_db)):
    """Reset Password

    Initiates account password resetting.
    """

    user = get_user_by_email(email=resetData.email, db=db)
    if not user:
        detail = f"User with email {resetData.email} does not exists"
        raise HTTPException(status_code=404, detail=detail)
    
    # TODO: create reset-token
    reset_token = ""

    # TODO: send email

    return {
        "message": "Password reset was successfully initiated",
        "details": {
            "reset_link": f"/auth/set-password/{reset_token}"
        }
    }


@router.put("/set-password/{reset_token}")
def set_password(reset_token: str, setPasswordData:PasswordSetSchema, db:Session = Depends(get_db)):
    # TODO: Decode token

    return {
        "message": "set password"
    }