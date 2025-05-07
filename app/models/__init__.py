# /your_project_root/app/models/__init__.py
# This file makes the 'models' directory a Python package.

from ..extensions import db

# Import models to ensure they are registered with SQLAlchemy
# This helps Flask-Migrate detect the models.
from .user import User
from .user_profile import UserProfile # Add this line to import the new UserProfile model
from .token_blocklist import TokenBlocklist
from .todo_item import TodoItem


# Add other models here as they are created
# from .post import Post
# from . (anchor related models for achievements, focus, plans will go here later)
