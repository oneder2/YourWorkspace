# /your_project_root/app/extensions.py
# Centralized place to initialize Flask extensions.
# This avoids circular imports and keeps app/__init__.py cleaner.

from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager
from flask_cors import CORS # CORS is often initialized directly in create_app

# Initialize SQLAlchemy - This object will be used to interact with the database.
# We don't associate it with the app here; that happens in the app factory.
db = SQLAlchemy()

# Initialize Flask-Migrate - Handles database schema migrations.
# Requires the SQLAlchemy db object and the Flask app instance upon initialization.
migrate = Migrate()

# Initialize Flask-Bcrypt - Used for hashing passwords securely.
bcrypt = Bcrypt()

# Initialize Flask-JWT-Extended - Manages JWT creation, verification, etc.
jwt = JWTManager()

# Note: Flask-CORS is typically initialized directly within the create_app factory
# because its configuration (like allowed origins) might depend on the app config.
# However, you could potentially initialize a basic CORS object here if preferred.
# cors = CORS()
