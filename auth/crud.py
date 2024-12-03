from sqlalchemy.orm import Session
from db.models import User
from .schemas import SignUpSchema, EmailStr



def create_user(userData:SignUpSchema,  db:Session):
    """Create user

    saves a new user to the database.

    Args:
        userData (SignUpSchema): Data to create a user
        db (Session): Database session
    """
    user = User()
    user.first_name = userData.first_name
    user.last_name = userData.last_name
    user. username = userData.username
    user.password = userData.password #TODO: has password
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


def get_user_by_email(email:EmailStr, db:Session):
    """get_user

    Args:
        email (EmailStr): email of a user
        db (Session): Database session
    """
    user = db.query(User).filter(User.email == email).first()
    return user
