import os
from datetime import timedelta


BASE_DIR = os.path.abspath(os.path.dirname(__file__))


class Config:
    """Base Configurations
    """
    API_TITLE = os.getenv("API_TITLE") or "RMI-API"
    API_VERSION = os.getenv("API_VERSION") or "1.0"
    API_DESCRIPTION = os.getenv("API_DESCRIPTION")

    SECRET_KEY = os.getenv("SECRET_KEY") or os.urandom(16)
    
    JWT_SECRET_KEY = SECRET_KEY
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(hours=1)

    SQLALCHEMY_TRACK_MODIFICATIONS = False

    RESTX_MASK_SWAGGER= False


class DevelopmentConfig(Config):
    """Development Configurations
    """
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = \
        'sqlite:////' + os.path.join(BASE_DIR, 'db/api.db')


class TestingConfig(Config):
    """Testing Configurations
    """
    TESTING = True
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = \
        'sqlite:////' + os.path.join(BASE_DIR, 'db/apitest.db')


class ProductionConfig(Config):
    """Production Configurations
    """
    DB_HOST = os.getenv("DB_HOST")
    DB_USER = os.getenv("DB_USER")
    DB_PASS = os.getenv("DB_PASS")
    DB_NAME = os.getenv("DB_NAME")
    SQLALCHEMY_DATABASE_URI = f"postgresql://{DB_USER}:{DB_PASS}@{DB_HOST}/{DB_NAME}"


configs = {
    "development": DevelopmentConfig,
    "testing": TestingConfig,
    "production": ProductionConfig
}

