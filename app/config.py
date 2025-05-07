# /your_project_root/app/config.py
# Defines configuration classes for different environments (development, testing, production).

import os
from dotenv import load_dotenv
from datetime import timedelta # Import timedelta for token expiration

# Calculate the base directory of the project (i.e., 'your_project_root')
basedir = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))

# Load environment variables from the .env file located at the project root
dotenv_path = os.path.join(basedir, '.env')
if os.path.exists(dotenv_path):
    load_dotenv(dotenv_path)
else:
    print("Warning: .env file not found at project root.")


class Config:
    """Base configuration class. Contains default settings."""
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'a-default-fallback-secret-key'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_ECHO = False # Usually False, can be True in DevelopmentConfig for debugging SQL

    # --- Flask-JWT-Extended Configuration ---
    JWT_TOKEN_LOCATION = ['headers']
    JWT_ALGORITHM = 'HS256'
    JWT_SECRET_KEY = os.environ.get('JWT_SECRET_KEY') or 'another-fallback-jwt-secret'
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(hours=1)
    JWT_REFRESH_TOKEN_EXPIRES = timedelta(days=30)

    # --- JWT Blocklist Configuration (for logout) ---
    JWT_BLOCKLIST_ENABLED = True
    JWT_BLOCKLIST_TOKEN_CHECKS = ['access', 'refresh']


    @staticmethod
    def init_app(app):
        pass


class DevelopmentConfig(Config):
    """Development-specific configuration."""
    DEBUG = True
    SQLALCHEMY_ECHO = True # Echo SQL statements for debugging
    SQLALCHEMY_DATABASE_URI = os.environ.get('DEV_DATABASE_URL') or \
        'sqlite:///' + os.path.join(basedir, 'instance', 'dev.sqlite')


class TestingConfig(Config):
    """Testing-specific configuration."""
    TESTING = True
    DEBUG = True # Often helpful during tests
    SECRET_KEY = 'test-secret-key' # Predictable key for testing
    JWT_SECRET_KEY = 'test-jwt-secret-key' # Use a predictable key for tests
    SQLALCHEMY_ECHO = False # Usually disable SQL echo during tests unless debugging specific SQL
    
    # Determine if TEST_DATABASE_URL is set, otherwise fallback to SQLite in-memory
    # This ensures that if TEST_DATABASE_URL is not set, we use SQLite for tests
    _test_db_url = os.environ.get('TEST_DATABASE_URL')
    if not _test_db_url:
        print("INFO: TEST_DATABASE_URL not set, using in-memory SQLite for testing.")
        SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'
    else:
        print(f"INFO: Using TEST_DATABASE_URL for testing: {_test_db_url}")
        SQLALCHEMY_DATABASE_URI = _test_db_url
    
    # Increased token expiry times for testing
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(seconds=30)  # Increased from 5
    JWT_REFRESH_TOKEN_EXPIRES = timedelta(minutes=1) # Increased from 10 seconds


class ProductionConfig(Config):
    """Production-specific configuration."""
    DEBUG = False
    TESTING = False
    SECRET_KEY = os.environ.get('SECRET_KEY')
    if not SECRET_KEY:
        raise ValueError("No SECRET_KEY set for production configuration")
    JWT_SECRET_KEY = os.environ.get('JWT_SECRET_KEY')
    if not JWT_SECRET_KEY:
        raise ValueError("No JWT_SECRET_KEY set for production configuration")

    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL')
    if not SQLALCHEMY_DATABASE_URI:
        raise ValueError("No DATABASE_URL set for production configuration")

    @classmethod
    def init_app(cls, app):
        Config.init_app(app)
        pass


config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig
}
