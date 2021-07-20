import os


class Config:
    """Base Configurations
    """
    SECRET_KEY = os.getenv("SECRET_KEY") or os.urandom(16)
    API_TITLE = os.getenv("API_TITLE") or "RMI-API"


class DevelopmentConfig(Config):
    """Development Configurations
    """
    DEBUG = True


class TestingConfig(Config):
    """Testing Configurations
    """
    TESTING = True


class ProductionConfig(Config):
    """Production Configurations
    """
    pass


configs = {
    "development": DevelopmentConfig,
    "testing": TestingConfig,
    "production": ProductionConfig
}

