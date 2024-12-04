from passlib.context import CryptContext


#TODO: Consider context saving/updating
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto") 


def generate_password_hash(password: str)-> str:
    """Generate a password hash

    Args:
        password (str): plain text to generate a hash on.
    Returns:
        str: hashed representation of the password.
    """
    return pwd_context.hash(password)


def verify_password(password: str, password_hash: str)-> bool:
    """Verify a password
    Check a password against a hash

    Args:
        password (str): plain text to generate a hash on.
        password_hash (str): hashed representation of the password
    
    Returns:
        bool: True if the password matches the hash, False otherwise.
    """
    return pwd_context.verify(password, password_hash)



def generate_access_token(payload: dict, time_to_expiry=1)-> str:
    """Generate access token

    Create a secure access token for authentication and authorization.

    Args:
        payload (dict): The claims to include in the token (e.g., user ID, roles).
        time_to_expiry (int, optional): The token's expiration time in seconds.

    Returns:
        str: A JSON Web Token (JWT) or similar token string, encoded and signed.
    """
    pass


def decode_access_token(token: str, secret_key: str)-> dict:
    """Decode access token

    Verifies an access token to extract its payload.

    Args:
        token (str):  The encoded access token (e.g., a JSON Web Token).
        secret_key (str): The secret key used to verify the token's signature.
    Returns:
        dict: The decoded payload (claims) of the token, such as user ID and roles.
    
    Raises:
        ValueError: If the token is invalid or the signature verification fails.
        ExpiredSignatureError: If the token has expired.
        DecodeError: If the token cannot be decoded due to format or corruption.
    """
    pass
