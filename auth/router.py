from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from db.db_deps import get_db
from .schemas import SignUpSchema, SignInSchema, PasswordResetSchema, PasswordSetSchema
from .crud import create_user, get_user_by_email, update_user_password
from .handler_password import verify_password
from .handler_token import generate_access_token, decode_access_token


router = APIRouter()


@router.post("/signup")
def signUp(signUpData: SignUpSchema, db:Session = Depends(get_db)):
    """Sign Up: 
    create a new user account.
    """

    user = get_user_by_email(email=signUpData.email, db=db)

    if user:
        detail = f"User with email {signUpData.email} exists."
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=detail)

    new_user = create_user(userData=signUpData, db=db)
    if new_user:
        return {
            "message": "Successful sign up.",
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
        detail = f"User with email {signInData.email} does not exists."
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=detail)
    
    if not verify_password(signInData.password, user.password):
        detail = "Invalid email or password."
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=detail)
    
    access_token = generate_access_token(user_data=user.uuid)

    return {
        "message": "Successful sign in.",
        "details": {
            "id": user.id,
            "uuid": user.uuid,
            "first_name": user.first_name,
            "last_name": user.last_name,
            "email": user.email
        },
        "token": {
            "access_token": access_token,
            "token_type": "bearer"
        }
    }


@router.post("/reset-password")
def reset_password(resetData: PasswordResetSchema, db:Session = Depends(get_db)):
    """Reset Password

    Initiates account password resetting.
    """

    user = get_user_by_email(email=resetData.email, db=db)
    if not user:
        detail = f"User with email {resetData.email} does not exists."
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=detail)
    
    reset_token = generate_access_token(user_data=user.uuid)

    # TODO: send email

    return {
        "message": "Password reset was successfully initiated.",
        "details": {
            "reset_token": reset_token
        }
    }


@router.put("/set-password/{reset_token}")
def set_password(reset_token: str, setPasswordData:PasswordSetSchema, db:Session = Depends(get_db)):
    
    if setPasswordData.password != setPasswordData.confirm_password:
        detail = f"Password and confirm password do no match."
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=detail)
    
    user_uuid = decode_access_token(token=reset_token)
    user = update_user_password(uuid=user_uuid, password=setPasswordData.password, db=db)

    return {
        "message": f"Password was successfully for '{user.email}'."
    }