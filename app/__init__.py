# /your_project_root/app/__init__.py
# Updated application factory using extensions from app/extensions.py

from flask import Flask
from flask_cors import CORS
import os

# Import configuration and initialized extensions
from .config import config
from .extensions import db, migrate, bcrypt, jwt # Import extension instances

def create_app(config_name='development'):
    """
    Application factory function.
    Configures and returns the Flask application instance.
    """
    app = Flask(__name__, instance_relative_config=True)

    # --- Load Configuration ---
    app.config.from_object(config[config_name])
    config[config_name].init_app(app)
    # Load instance config if exists (e.g., app.config.from_pyfile('config.py', silent=True))

    # --- Initialize Extensions with App Context ---
    # Pass the Flask app instance to the init_app method of each extension
    db.init_app(app)
    migrate.init_app(app, db) # Flask-Migrate needs both app and db
    bcrypt.init_app(app)
    jwt.init_app(app)

    # Initialize CORS (can still be done here or using the instance from extensions.py)
    CORS(app, resources={r"/api/*": {"origins": "*"}}) # Adjust origins for production

    # --- Register Blueprints ---
    from .api.auth_bp import auth_bp
    from .api.blog_bp import blog_bp
    from .api.todo_bp import todo_bp
    from .api.ai_bp import ai_bp

    app.register_blueprint(auth_bp, url_prefix='/api/v1/auth')
    app.register_blueprint(blog_bp, url_prefix='/api/v1/blog')
    app.register_blueprint(todo_bp, url_prefix='/api/v1/todo')
    app.register_blueprint(ai_bp, url_prefix='/api/v1/ai')

    # --- Database Creation (within Application Context) ---
    # It's good practice to ensure the database tables are created.
    # Flask-Migrate handles this, but this ensures creation if migrations aren't run yet.
    # Use app.app_context() to work within the application context.
    with app.app_context():
        # Import models here to avoid circular imports earlier
        # This ensures models are known to SQLAlchemy before create_all is called
        from . import models # Or explicitly import needed models: from .models.user import User

        # Create database tables for our data models if they don't exist
        # Note: Flask-Migrate is the preferred way to manage schema changes long-term.
        db.create_all() # Uncomment this line if you want Flask to create tables directly
                          # Often commented out when using Flask-Migrate exclusively for schema management.

    # --- Simple Root Route ---
    @app.route('/')
    def index():
        return "Flask API Backend is running!"

    return app
