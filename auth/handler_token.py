from datetime import datetime, timedelta, timezone
from typing import Optional
from fastapi import HTTPException, status
from jose import jwt, JWTError
from config import TOKEN_ALGORITHM, TOKEN_EXPIRY_MINUTES, SECRET_KEY



def generate_access_token(user_data: str, 
                          time_to_expiry: Optional[timedelta] = TOKEN_EXPIRY_MINUTES)-> str:
    """Generate access token

    Create a secure access token for authentication and authorization.

    Args:
        user_data (str): The claims to include in the token (e.g., user ID, roles).
        time_to_expiry (timedelta, optional): The token's expiration time in seconds.

    Returns:
        str: A JSON Web Token (JWT) or similar token string, encoded and signed.
    """
   
    issued_at =  datetime.now(timezone.utc)
    expire  = issued_at + timedelta(minutes=time_to_expiry)
    payload = {
        "sub": user_data,
        "exp": expire,
        "iat": issued_at
    }

    return jwt.encode(payload, SECRET_KEY, algorithm=TOKEN_ALGORITHM)


def decode_access_token(token: str)-> str:
    """Decode access token

    Verifies an access token to extract its payload.

    Args:
        token (str):  The encoded access token (e.g., a JSON Web Token).
    Returns:
        str: The decoded user_data (claims["sub"]) of the token, such as user ID and roles.
    """
    
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[TOKEN_ALGORITHM])
        user_data = payload.get("sub")
        if user_data is None:
            raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="You are not authorized.")
        
    except JWTError:
        raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="You are not authorized, error.")
    return user_data