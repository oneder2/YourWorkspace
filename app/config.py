# /your_project_root/app/config.py
# Defines configuration classes for different environments.

import os
from datetime import timedelta
from dotenv import load_dotenv

# Determine the base directory of the project (where run.py is)
# __file__ points to the location of config.py (app/config.py)
# os.path.dirname(__file__) gives the 'app' directory
# os.path.dirname(os.path.dirname(__file__)) gives the project root directory
basedir = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))

# Load environment variables from .env file located at the project root
dotenv_path = os.path.join(basedir, '.env')
if os.path.exists(dotenv_path):
    load_dotenv(dotenv_path)
else:
    print("Warning: .env file not found at project root.") # Optional warning

class Config:
    """Base configuration class. Contains default settings."""
    # Secret key for session management, CSRF protection, etc.
    # CRITICAL: Load from environment variable in production!
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'a-default-fallback-secret-key-replace-me'

    # Database configuration (set in subclasses)
    SQLALCHEMY_DATABASE_URI = None
    # Disable SQLAlchemy event system if not needed, saves resources
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # JWT Configuration (using Flask-JWT-Extended)
    JWT_SECRET_KEY = os.environ.get('JWT_SECRET_KEY') or 'a-default-jwt-secret-key-replace-me'
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(hours=1) # Access token lifetime
    JWT_REFRESH_TOKEN_EXPIRES = timedelta(days=30) # Refresh token lifetime
    # Consider storing tokens in cookies for web SPAs (set JWT_TOKEN_LOCATION = ['cookies'])
    # JWT_TOKEN_LOCATION = ['headers'] # Default: Expect tokens in Authorization header
    # JWT_COOKIE_SECURE = False # Set True in production if using HTTPS
    # JWT_COOKIE_CSRF_PROTECT = True # Recommended if using cookies

    # Add other base configurations common to all environments
    # Example: Mail server settings, logging configuration, etc.
    # MAIL_SERVER = os.environ.get('MAIL_SERVER')
    # MAIL_PORT = int(os.environ.get('MAIL_PORT') or 25)
    # MAIL_USE_TLS = os.environ.get('MAIL_USE_TLS') is not None
    # MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
    # MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')
    # ADMINS = ['your-email@example.com']

    @staticmethod
    def init_app(app):
        """Perform application-specific initialization based on config."""
        # Example: Configure logging
        import logging
        from logging.handlers import RotatingFileHandler
        if not app.debug and not app.testing:
            # Configure file logging for production
            if not os.path.exists('logs'):
                os.mkdir('logs')
            file_handler = RotatingFileHandler('logs/app.log', maxBytes=10240, backupCount=10)
            file_handler.setFormatter(logging.Formatter(
                '%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]'))
            file_handler.setLevel(logging.INFO)
            app.logger.addHandler(file_handler)
        
            app.logger.setLevel(logging.INFO)
            app.logger.info('Application startup')


class DevelopmentConfig(Config):
    """Development-specific configuration."""
    DEBUG = True
    # Example using SQLite for simple development setup
    # Ensure the 'instance' folder exists at the project root
    # SQLALCHEMY_DATABASE_URI = os.environ.get('DEV_DATABASE_URL') or \
    #     'sqlite:///' + os.path.join(basedir, 'instance', 'dev.db')
    # Or use PostgreSQL:
    SQLALCHEMY_DATABASE_URI = os.environ.get('DEV_DATABASE_URL') or \
        'postgresql://your_dev_user:your_dev_password@localhost:5432/your_dev_db'


class TestingConfig(Config):
    """Testing-specific configuration."""
    TESTING = True
    DEBUG = True # Often helpful during tests to get more detailed errors
    # Use a predictable secret key for testing purposes
    SECRET_KEY = 'test-secret-key'
    JWT_SECRET_KEY = 'test-jwt-secret-key'
    # Use a separate database for testing (e.g., in-memory SQLite or a dedicated test DB)
    SQLALCHEMY_DATABASE_URI = os.environ.get('TEST_DATABASE_URL') or \
        'sqlite:///:memory:' # In-memory SQLite is fast for tests
    # Disable CSRF protection in tests if using cookies for tokens
    # WTF_CSRF_ENABLED = False
    # JWT_COOKIE_CSRF_PROTECT = False


class ProductionConfig(Config):
    """Production-specific configuration."""
    DEBUG = False
    TESTING = False
    # Ensure SECRET_KEY and JWT_SECRET_KEY are set via environment variables in production!
    SECRET_KEY = os.environ.get('SECRET_KEY') # Must be set
    JWT_SECRET_KEY = os.environ.get('JWT_SECRET_KEY') # Must be set

    # Database URL must be provided via environment variable in production
    # TODO the database url shoule be replaced to production url in formal condition, reference .env
    SQLALCHEMY_DATABASE_URI = os.environ.get('TEST_DATABASE_URL')
    if not SQLALCHEMY_DATABASE_URI:
        raise ValueError("No DATABASE_URL set for production environment")

    # Security enhancements for production
    # SESSION_COOKIE_SECURE = True # Ensure cookies only sent over HTTPS
    # REMEMBER_COOKIE_SECURE = True
    # SESSION_COOKIE_HTTPONLY = True # Prevent client-side JS access to session cookie
    # REMEMBER_COOKIE_HTTPONLY = True
    # SESSION_COOKIE_SAMESITE = 'Lax' # Mitigate CSRF
    # JWT_COOKIE_SECURE = True # Ensure JWT cookies only sent over HTTPS
    # Add other production settings: logging level, trusted proxies (if behind one)


# Dictionary to map configuration names to their classes
config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig # Default configuration to use if none specified
}
