from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from db.db_deps import get_db
from .schemas import SignUpSchema, SignInSchema, PasswordResetSchema, PasswordSetSchema
from .crud import create_user, get_user_by_email, update_user_password
from .handler_password import verify_password
from .handler_token import generate_access_token, decode_access_token


router = APIRouter()


@router.post("/signup", status_code=201)
def signUp(signUpData: SignUpSchema, db:Session = Depends(get_db)):
    """Sign Up: 
    create a new user account.
    """

    user = get_user_by_email(email=signUpData.email, db=db)

    if user:
        detail = {
            "message": f"User with email {signUpData.email} exists.",
            "action": "Use another email",
            "success": False
        }
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=detail)

    new_user = create_user(userData=signUpData, db=db)
    if new_user:
        return {
            "details": {
                "message": "Successful sign up.",
                "action": "Use email & password to sign-in",
                "success": True,
                "first_name": new_user.first_name,
                "last_name": new_user.last_name,
                "email": new_user.email
            },
        }


@router.post("/signin", status_code=200)
def signIn(signInData: SignInSchema, db:Session = Depends(get_db)):
    """Sign in
    Assigns an already signed up user a auth token for session  management.
    """
    user = get_user_by_email(email=signInData.email, db=db)

    if not user:
        detail = {
            "message": "Invalid email or password.",
            "action": "Review your sign-in email & password",
            "success": False
        }
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=detail)
    
    if not verify_password(signInData.password, user.password):
        detail = {
            "message": "Invalid email or password.",
            "action": "Review your sign-in email & password",
            "success": False
        }
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=detail)
    
    access_token = generate_access_token(user_data=user.uuid)

    return {
        "details": { # TODO: remove details
            "message": "Successful sign in.",
            "action": "Your session has been started",
            "success": True,
            "user_id": user.id,
            "uuid": user.uuid,
            "first_name": user.first_name,
            "last_name": user.last_name,
            "email": user.email,
            "token": { # TODO: Add refresh token
                "access_token": access_token,
                "token_type": "bearer"
            },
            
        },
    }


@router.post("/reset-password")
def reset_password(resetData: PasswordResetSchema, db:Session = Depends(get_db)):
    """Reset Password

    Initiates account password resetting.
    """

    user = get_user_by_email(email=resetData.email, db=db)
    if not user:
        detail = {
            "message": f"User with email {resetData.email} does not exists.",
            "action": "Review the reset password",
            "success": False
        }
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=detail)
    
    reset_token = generate_access_token(user_data=user.uuid)

    # TODO: send email

    return {
        "details": {
            "message": "Password reset was successfully initiated.",
            "action": "Review your mail box",
            "success": True,
            "reset_token": reset_token
        },
    }


@router.put("/set-password/{reset_token}")
def set_password(reset_token: str, setPasswordData:PasswordSetSchema, db:Session = Depends(get_db)):
    
    # if setPasswordData.password != setPasswordData.confirm_password:
    #     detail = f"Password and confirm password do no match."
    #     raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=detail)
    
    try:
        user_uuid = decode_access_token(token=reset_token)
    except:
        detail = {
            "message": "Something went wrong with your request",
            "action": "Review your request and try again",
            "success": True,
        }
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=detail)
    
    user = update_user_password(uuid=user_uuid, password=setPasswordData.password, db=db)
    
    return {
        "details": {
            "message": f"Password was successfully for '{user.email}'.",
            "action": "Use new password to sign-in",
            "success": True
        },
    }
