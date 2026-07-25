from datetime import datetime, timezone
from fastapi import APIRouter, Depends, HTTPException, status, Response, Request
from sqlalchemy.orm import Session
from typing import Optional
from db.db_deps import get_db
from config import REFRESH_TOKEN_EXPIRE_DAYS
from .schemas import SignUpSchema, SignInSchema, PasswordResetSchema, \
    PasswordSetSchema, TokenResponseSchema, RefreshTokenRequest, UserSchema
from .crud import create_user, get_user_by_email, update_user_password, \
    save_refresh_token, get_refresh_token, get_user_by_uuid, revoke_refresh_tokens
from .handler_password import verify_password
from .handler_token import generate_access_token, decode_access_token, \
    create_refresh_token
from .deps_auth import get_current_user


router = APIRouter()


@router.post("/signup", status_code=status.HTTP_201_CREATED)
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


@router.post("/signin", status_code=status.HTTP_200_OK)
def signIn(signInData: SignInSchema, response: Response, db:Session = Depends(get_db)):
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
        raise HTTPException(status_code=status.HTTP_401_NOT_FOUND, detail=detail)
    
    if not verify_password(signInData.password, user.password):
        detail = {
            "message": "Invalid email or password.",
            "action": "Review your sign-in email & password",
            "success": False
        }
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=detail)
    
    access_token = generate_access_token(user_data=user.uuid)
    
    # Save access token
    refresh_token = create_refresh_token(user_data=user.uuid)
    save_refresh_token(user_uuid=user.uuid, token=refresh_token, db=db)

    # Set refresh token as HttpOnly cookie
    response.set_cookie(
        key="refresh_token",
        value=refresh_token,
        httponly=True,
        secure=True,
        samesite="strict",
        max_age=REFRESH_TOKEN_EXPIRE_DAYS * 24 * 60 * 60,
        domain=None  # TODO Use same domain
    )


    return {
        "details": {
            "message": "Successful sign in.",
            "action": "Your session has been started",
            "success": True,
            # "user_id": user.id,
            # "uuid": user.uuid,
            # "first_name": user.first_name,
            # "last_name": user.last_name,
            # "email": user.email,
            "token": {
                "access_token": access_token,
                "refresh_token": refresh_token,
                "token_type": "bearer"
            },
        },
    }


@router.post("/refresh", status_code=status.HTTP_200_OK)
async def refetch_access_token(
    refresh_data: Optional[RefreshTokenRequest] = None,
    request: Request = None,
    db: Session = Depends(get_db)
):
    token = None
    if refresh_data and refresh_data.refresh_token:
        token = refresh_data.refresh_token
    else:
        # Get from cookie
        token = request.cookies.get("refresh_token")

    if not token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail={
                "message": "Refresh token missing",
                "action": "Ensure you include token & try again",
                "success": False
            }
        )

    db_refresh_token = get_refresh_token(token=token, db=db)

    if not db_refresh_token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail={
                "message": "Invalid refresh token",
                "action": "Try logging in again",
                "success": False
            }
        )

    if  db_refresh_token.expires_at.replace(tzinfo=timezone.utc) < datetime.now(timezone.utc):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail={
                "message": "Refresh token expired",
                "action": "Try logging in again",
                "success": False
            }
        )

    user = get_user_by_uuid(uuid=db_refresh_token.user_uuid, db=db)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail={
                "message": "User not found",
                "action": "Try logging in again",
                "success": False
            }
        )

    access_token = generate_access_token(user_data=user.uuid)

    return {
        "details":{
            "message": "Successful token refresh",
            "action": "Continue with your session",
            "success": True,
            "token": {
                "access_token": access_token,
                "refresh_token": token,
                "token_type": "bearer"
            },
        }
    }


@router.post("/logout", status_code=status.HTTP_204_NO_CONTENT)
async def logout( 
    current_user: UserSchema = Depends(get_current_user),
    request: Request = None, 
    response: Response = None, 
    db: Session = Depends(get_db)
    
):
    # Revoke user refresh tokens
    revoke_refresh_tokens(user_uuid=current_user.uuid, db=db)

    # Clear cookie
    response.delete_cookie("refresh_token")

    return {
        "details": {
            "message": "Logout was successful.",
            "action": "Consider logging in again to continue using the app.",
            "success": True
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
