# /your_project_root/app/models/user.py
# Defines the User database model.

from ..extensions import db, bcrypt
import datetime # Import datetime module
from .user_profile import UserProfile

class User(db.Model):
    """
    User model for storing user accounts.
    """
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)

    created_at = db.Column(db.DateTime, default=lambda: datetime.datetime.now(datetime.timezone.utc))
    updated_at = db.Column(db.DateTime,
                           default=lambda: datetime.datetime.now(datetime.timezone.utc),
                           onupdate=lambda: datetime.datetime.now(datetime.timezone.utc))

    # --- Relationship to UserProfile (One-to-One) ---
    # 'profile' attribute will allow access to the UserProfile record.
    # 'cascade="all, delete-orphan"' means if a User is deleted, their UserProfile is also deleted.
    # 'uselist=False' on the UserProfile side's relationship definition establishes one-to-one.
    # Here, `back_populates` links this to the 'user' attribute in UserProfile.
    profile = db.relationship('UserProfile', back_populates='user', uselist=False, cascade="all, delete-orphan")

    # Relationships to other models
    # todo_items = db.relationship('TodoItem', backref='owner', lazy='dynamic') # Example if backref was used on TodoItem
    # posts = db.relationship('Post', backref='author', lazy='dynamic')

    def __init__(self, username, email, password):
        """Constructor for User model."""
        self.username = username
        self.email = email
        self.set_password(password)
        # Automatically create an empty UserProfile when a new User is created
        self.profile = UserProfile()


    def set_password(self, password):
        """Hashes the provided password and stores it."""
        self.password_hash = bcrypt.generate_password_hash(password).decode('utf-8')

    def check_password(self, password):
        """Checks if the provided password matches the stored hash."""
        return bcrypt.check_password_hash(self.password_hash, password)

    def __repr__(self):
        """String representation of the User object."""
        return f'<User {self.username}>'

    # Method to get user data including profile information
    def to_dict_with_profile(self):
        """Converts User and its profile to a dictionary."""
        profile_data = self.profile.to_dict() if self.profile else {}
        return {
            'id': self.id,
            'username': self.username,
            'email': self.email,
            'created_at': self.created_at.isoformat() + 'Z',
            'updated_at': self.updated_at.isoformat() + 'Z',
            'profile': profile_data # Embed profile data
        }
