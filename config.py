import os
from dotenv import load_dotenv


load_dotenv()


ENVIRONMENT = os.getenv("ENVIRONMENT")

SQLALCHEMY_DATABASE_URI = "sqlite:///app.db"
DATABASE_CONNECT_ARGS = {"check_same_thread": False}

SECRET_KEY = os.getenv("SECRET_KEY", "Provide123StrongerKey")
TOKEN_ALGORITHM = "HS256"
TOKEN_EXPIRY_MINUTES = 60
