from sqlalchemy.orm import Session
from db.models import User
from .schemas import SignUpSchema, EmailStr
from .handler_password import generate_password_hash



def create_user(userData:SignUpSchema,  db:Session)-> User:
    """Create user

    saves a new user to the database.

    Args:
        userData (SignUpSchema): Data to create a user
        db (Session): Database session

    Returns:
        User: A database model representing a user.
    """
    user = User()
    user.first_name = userData.first_name
    user.last_name = userData.last_name
    user.email = userData.email
    user.password = generate_password_hash(userData.password)
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


def get_user_by_email(email:EmailStr, db:Session)-> User:
    """get_user

    Args:
        email (EmailStr): email of a user
        db (Session): Database session
    
    Returns:
        User: A database model representing a user.
    """
    user = db.query(User).filter(User.email == email).first()
    return user


def get_user_by_uuid(uuid: str, db:Session)-> User:
    """Get user by uuid

    Args:
        uuid (str): A string representing a uuid .
        db (Session): Database session.

    Returns:
        User: A database model representing a user.
    """

    user = db.query(User).filter(User.uuid == uuid).first()
    return user


def update_user_password(uuid: str, password: str, db:Session)-> User:
    """Update user password

    Args:
        uuid (str): A string representing a uuid. 
        password (str):  plain text to generate a hash on.
        db (Session): Database session.
    
    Returns:
        User: A database model representing a user.
    """

    user = get_user_by_uuid(uuid=uuid, db=db)
    user.password = generate_password_hash(password=password)
    db.add(user)
    db.commit()
    db.refresh(user)
    return user
