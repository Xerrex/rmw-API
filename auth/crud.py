from datetime import datetime, timezone, timedelta
from sqlalchemy.orm import Session
from db.models import User, RefreshToken
from .schemas import SignUpSchema, EmailStr, SaveRefreshToken
from .handler_password import generate_password_hash
from config import REFRESH_TOKEN_EXPIRE_DAYS



def create_user(userData:SignUpSchema,  db:Session)-> User:
    """Create user

    saves a new user to the database.

    Args:
        userData (SignUpSchema): Data to create a user.
        db (Session): Database session.

    Returns:
        User: A database object representing a user.
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
    """Get_user

    Args:
        email (EmailStr): email of a user.
        db (Session): Database session.
    
    Returns:
        User: A database object representing a user.
    """
    user = db.query(User).filter(User.email == email).first()
    return user


def get_user_by_uuid(uuid: str, db:Session)-> User:
    """Get user by uuid

    Args:
        uuid (str): A string representing a uuid.
        db (Session): Database session.

    Returns:
        User: A database object representing a user.
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
        User: A database object representing a user.
    """

    user = get_user_by_uuid(uuid=uuid, db=db)
    user.password = generate_password_hash(password=password)
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


def save_refresh_token(user_uuid: str, token: str, db:Session) -> RefreshToken:
    """Save refresh token

    Args:
        tokenData (SaveRefreshToken): Data used to define a new token

    Returns:
        RefreshToken: A database object representing a refresh token.
    """

    refresh_token = RefreshToken(
        user_uuid = user_uuid,
        token =  token,
        expires_at = datetime.now(timezone.utc) + timedelta(days=REFRESH_TOKEN_EXPIRE_DAYS)
    )

    db.add(refresh_token)
    db.commit()


def get_refresh_token(token: str, db:Session)-> RefreshToken:
    """Get refresh token

    Args:
        token (str):A string representing an auth token.
        db (Session): Database session.

    Returns:
        RefreshToken: A database object representing refresh token.
    """

    db_token = db.query(RefreshToken).filter(
        RefreshToken.token == token,
        RefreshToken.is_revoked == False
    ).first()

    return db_token


def revoke_refresh_tokens(user_uuid: str, db:Session)-> None:
    """Revoke refresh tokens

    Args:
        user_uuid (str): A string representing a uuid unique to a user.
        db (Session):  Database session.
    """

    db.query(RefreshToken).filter(RefreshToken.user_uuid == user_uuid).update(
        {"is_revoked": True}
    )
    db.commit()