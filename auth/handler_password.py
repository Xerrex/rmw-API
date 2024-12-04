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
        password_hash (str): hashed representation of the password.
    
    Returns:
        bool: True if the password matches the hash, False otherwise.
    """
    return pwd_context.verify(password, password_hash)