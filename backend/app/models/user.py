# /your_project_root/app/models/user.py
# Defines the User database model.

from ..extensions import db, bcrypt
import datetime
from .base import BaseModel
from .user_profile import UserProfile
from typing import Dict, Any, Optional

class User(BaseModel):
    """
    User model for storing user accounts.
    Inherits common fields and methods from BaseModel.
    """
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)

    # --- Relationship to UserProfile (One-to-One) ---
    # 'profile' attribute will allow access to the UserProfile record.
    # 'cascade="all, delete-orphan"' means if a User is deleted, their UserProfile is also deleted.
    # 'uselist=False' on the UserProfile side's relationship definition establishes one-to-one.
    # Here, `back_populates` links this to the 'user' attribute in UserProfile.
    profile = db.relationship('UserProfile', back_populates='user', uselist=False, cascade="all, delete-orphan")

    # Relationships to other models
    # todo_items = db.relationship('TodoItem', backref='owner', lazy='dynamic') # Example if backref was used on TodoItem
    # posts = db.relationship('Post', backref='author', lazy='dynamic')

    def __init__(self, username: str, email: str, password: str):
        """Constructor for User model."""
        self.username = username
        self.email = email
        self.set_password(password)
        # Automatically create an empty UserProfile when a new User is created
        self.profile = UserProfile()

    def set_password(self, password: str) -> None:
        """Hashes the provided password and stores it."""
        self.password_hash = bcrypt.generate_password_hash(password).decode('utf-8')

    def check_password(self, password: str) -> bool:
        """Checks if the provided password matches the stored hash."""
        return bcrypt.check_password_hash(self.password_hash, password)

    def __repr__(self) -> str:
        """String representation of the User object."""
        return f'<User {self.username}>'

    def to_dict(self) -> Dict[str, Any]:
        """Converts the User instance to a dictionary (without profile)."""
        return {
            'id': self.id,
            'username': self.username,
            'email': self.email,
            'created_at': self.format_datetime(self.created_at),
            'updated_at': self.format_datetime(self.updated_at),
        }

    # Method to get user data including profile information
    def to_dict_with_profile(self) -> Dict[str, Any]:
        """Converts User and its profile to a dictionary."""
        profile_data = self.profile.to_dict() if self.profile else {}
        user_data = self.to_dict()
        user_data['profile'] = profile_data
        return user_data
