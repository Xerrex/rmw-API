import os
from dotenv import load_dotenv


load_dotenv()


ENVIRONMENT = os.getenv("ENVIRONMENT")

SQLALCHEMY_DATABASE_URI = "sqlite:///app.db"
DATABASE_CONNECT_ARGS = {"check_same_thread": False} if ENVIRONMENT=="DEV" else None

SECRET_KEY = os.getenv("SECRET_KEY", "01cbdc2656463a93819efe9030237ae0f7")
TOKEN_ALGORITHM = "HS256"
TOKEN_EXPIRY_MINUTES = 60
