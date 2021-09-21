from flask import Flask

from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_jwt_extended import JWTManager

db = SQLAlchemy()
jwt = JWTManager()

def ext_init_app(app: Flask):
    """Initialize apps with the Flask App

    Args:
        app (Flask): Instance of a Flask app
    """
    db.init_app(app)
    Migrate(app, db) # handle db migrations
    jwt.init_app(app)# Handles the JWT
    
    