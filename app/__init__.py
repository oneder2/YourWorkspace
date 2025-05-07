# /your_project_root/app/__init__.py
# Updated application factory using extensions from app/extensions.py

from flask import Flask
from flask_cors import CORS # CORS is often initialized directly in create_app
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
    config[config_name].init_app(app) # Optional: Allow config class to perform init tasks
    # Load sensitive config from instance/config.py if it exists
    # Example: app.config.from_pyfile('config.py', silent=True)

    # --- Initialize Extensions with App Context ---
    db.init_app(app)
    migrate.init_app(app, db) # Flask-Migrate needs both app and db
    bcrypt.init_app(app)
    jwt.init_app(app) # Initialize JWTManager

    # Initialize CORS
    CORS(app, resources={r"/api/*": {"origins": "*"}}) # Adjust origins for production

    # --- Register Blueprints ---
    from .api.auth_bp import auth_bp
    from .api.blog_bp import blog_bp # Assuming this exists or will be added
    from .api.todo_bp import todo_bp # Import the new todo_bp
    from .api.ai_bp import ai_bp   # Assuming this exists or will be added

    app.register_blueprint(auth_bp, url_prefix='/api/v1/auth')
    app.register_blueprint(blog_bp, url_prefix='/api/v1/blog')
    app.register_blueprint(todo_bp, url_prefix='/api/v1/todo') # Register todo_bp
    app.register_blueprint(ai_bp, url_prefix='/api/v1/ai')

    # --- Database Creation (within Application Context) ---
    # This section is typically handled by Flask-Migrate.
    # If you want to ensure tables are created on app start (e.g., for SQLite in-memory tests
    # without migrations), you might uncomment db.create_all().
    # For PostgreSQL with migrations, this is usually not needed here.
    # with app.app_context():
    #     # Import models here to avoid circular imports earlier
    #     from . import models # Or explicitly import needed models
    #     db.create_all()

    # --- Simple Root Route ---
    @app.route('/')
    def index():
        return "Flask API Backend is running!"

    return app
