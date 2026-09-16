import os
from dotenv import load_dotenv


load_dotenv()


ENVIRONMENT: str = os.getenv("ENVIRONMENT")

SQLALCHEMY_DATABASE_URI: str = "sqlite:///app.db"
DATABASE_CONNECT_ARGS = {"check_same_thread": False} if ENVIRONMENT=="DEV" else None

SECRET_KEY: str = os.getenv("SECRET_KEY", "01cbdc2656463a93819efe9030237ae0f7")
TOKEN_ALGORITHM: str = "HS256"
TOKEN_EXPIRY_MINUTES: int = 60
REFRESH_TOKEN_EXPIRE_DAYS: int = 7

origins = os.getenv("ALLOWED_ORIGINS")
ALLOWED_ORIGINS = origins.split(",") if origins else []
