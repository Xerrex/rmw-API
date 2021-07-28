from .models import User


def create_user(name, username, email, password):
    """Create a new User

    Args:
        name (String): name of the User
        username (String): a unique name to identify user
        email (String): an Email formated string
        password (String): The secret key to authenticate a user.
    """
    user = User(name, username, email, password)
    user.save()


def get_user_by_id(id):
    """Fetch a User based on the ID

    Args:
        id (Integer): unique Integer identifer of a User
    Return:
        user (User): User model
    """
    user = User.query.get(id)
    return user


def get_user_by_username(username):
    """Fetch User based on the username

    Args:
        username (String): a unique name to identify user

    Returns:
        user (User): User model
    """
    user = User.query.filter_by(username=username).first()
    return user


def get_user_by_email(email):
    """Fetch a user based on the Email
    """
    user = User.query.filter_by(email=email).first()
    return user