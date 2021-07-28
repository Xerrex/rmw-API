from datetime import datetime

from werkzeug.security import check_password_hash, \
    generate_password_hash

from flask_jwt_extended import create_access_token

from app.utils.exts import db


class User(db.Model):
    """The User Model
    """
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    username = db.Column(db.String(120), unique=True, nullable=False)
    email = db.Column(db.String(255), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    last_login = db.Column(db.DateTime, default=datetime.utcnow)

    def __init__(self, name, username, email, password):
        """Defines how to create a new User

        Args:
            name (String): name of the User
            username (String): a unique name to identify user
            email (String): an Email formated string
            password (String): The secret key to authenticate a user
        """

        self.name = name
        self.username = username
        self.email = email
        self.password = generate_password_hash(password)
    
    def save(self):
        """Method to save or update user details
        """
        db.session.add(self)
        db.session.commit()

    def __repr__(self) -> str:
        """Define how a User is printed
        """
        return f'User-{self.username}'
    
    def verify_password(self, password):
        """Verify the password of a user

        Args:
            password (String): The secret key to authenticate a user

        Returns:
            bool : True or False
        """
        
        return check_password_hash(self.password, password)
    
    def generate_access_token(self):
        """Create a JWT access token
        """
        identity = self.username
        access_token = create_access_token(identity=identity)
        return access_token

