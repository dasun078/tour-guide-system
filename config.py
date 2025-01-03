import os

class Config:
    """Base configuration shared across all environments."""
    SECRET_KEY = os.environ.get('SECRET_KEY', '123456789')  # Ensure you replace it with a secure key
    SQLALCHEMY_TRACK_MODIFICATIONS = False  # Disable SQLAlchemy event system for performance
    SESSION_TYPE = 'filesystem'  # Flask-Session configuration
    GOOGLE_MAPS_API_KEY = os.environ.get('GOOGLE_MAPS_API_KEY', 'your_default_google_maps_api_key')

    @staticmethod
    def init_app(app):
        """Perform any additional configuration setup."""
        pass


class DevelopmentConfig(Config):
    """Configuration for development environment."""
    DEBUG = True  # Enable debug mode for detailed error pages
    SQLALCHEMY_DATABASE_URI = os.environ.get(
        'SQLALCHEMY_DATABASE_URI',
        'mysql+pymysql://root:Dasun@070@127.0.0.1:3306/tour_guide_system'
    )  # Default database URL for development


class TestingConfig(Config):
    """Configuration for testing environment."""
    TESTING = True  # Enable testing mode
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'  # Use in-memory SQLite for faster tests
    WTF_CSRF_ENABLED = False  # Disable CSRF protection for easier testing of forms
    DEBUG = True


class ProductionConfig(Config):
    """Configuration for production environment."""
    DEBUG = False  # Ensure debug mode is off in production
    SQLALCHEMY_DATABASE_URI = os.environ.get(
        'SQLALCHEMY_DATABASE_URI',
        'mysql+pymysql://root:Dasun@070@127.0.0.1:3306/tour_guide_system'
    )  # Database URL for production environment

    @staticmethod
    def init_app(app):
        """Configure production-specific behavior."""
        import logging
        from logging.handlers import RotatingFileHandler

        # Set up logging for production
        if not os.path.exists('logs'):
            os.mkdir('logs')
        file_handler = RotatingFileHandler('logs/error.log', maxBytes=10240, backupCount=10)
        file_handler.setLevel(logging.ERROR)
        app.logger.addHandler(file_handler)


# Map environment names to configuration classes
config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig  # Default configuration if no environment is specified
}
