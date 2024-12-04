from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session
from jose import JWTError
from db.db_deps import get_db
from .crud import get_user_by_uuid
from .handler_token import decode_access_token
from .schemas import UserSchema


security = HTTPBearer()


def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security), 
                     db:Session = Depends(get_db))-> UserSchema:
    """Get current user

    Args:
        credentials (HTTPAuthorizationCredentials): The Authorization header containing the Bearer token. 
            This is automatically populated by FastAPI's dependency injection when using the `Depends` function.
    
    Returns:
        UserSchema: The user details wrapped in a Pydantic model.
    
    Raises:
        HTTPException: If the token is missing, invalid, expired, or if the corresponding user cannot be found.
            - Status Code: 401 (Unauthorized)
            - Detail: "Invalid or expired token"
            - Headers: {"WWW-Authenticate": "Bearer"}
    
    Expected Usage:
        This function is used as a dependency for FastAPI endpoints to enforce token-based authentication. 
        For example:
        ```
        @app.get("/secure-endpoint", dependencies=[Depends(get_current_user)])
        def secure_endpoint(current_user: User = Depends(get_current_user)):
            return {"message": f"Welcome, {current_user.name}"}
        ```
    Example Authorization Header:
        ```
        Authorization: Bearer <your_token_here>
    """

    try:
        token = credentials.credentials
        user_uuid = decode_access_token(token=token)
        user = get_user_by_uuid(uuid=user_uuid, db=db)
        user_out = UserSchema.model_validate(user)
        return  user_out
    
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired token",
            headers={"WWW-Authenticate": "Bearer"},
        )