import os
from re import DEBUG


class Config:
    """Base Configurations
    """
    API_TITLE = os.getenv("API_TITLE") or "RMI-API"
    API_VERSION = os.getenv("API_VERSION") or "1.0"
    API_DESCRIPTION = os.getenv("API_DESCRIPTION")

    SECRET_KEY = os.getenv("SECRET_KEY") or os.urandom(16)


class DevelopmentConfig(Config):
    """Development Configurations
    """
    DEBUG = True


class TestingConfig(Config):
    """Testing Configurations
    """
    TESTING = True
    DEBUG = True


class ProductionConfig(Config):
    """Production Configurations
    """
    pass


configs = {
    "development": DevelopmentConfig,
    "testing": TestingConfig,
    "production": ProductionConfig
}

