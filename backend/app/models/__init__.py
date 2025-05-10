# /your_project_root/app/models/__init__.py
# This file makes the 'models' directory a Python package.

from ..extensions import db

# Import models to ensure they are registered with SQLAlchemy
# This helps Flask-Migrate detect the models.
from .user import User
from .token_blocklist import TokenBlocklist
from .todo_item import TodoItem
from .user_profile import UserProfile
from .achievement import Achievement
# from .current_focus_item import CurrentFocusItem # REMOVE THIS LINE
from .future_plan import FuturePlan


# Add other models here as they are created
# from .post import Post
