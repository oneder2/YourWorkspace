# /your_project_root/app/models/user.py
# Defines the User database model.

from ..extensions import db, bcrypt
import datetime # Import datetime module

class User(db.Model):
    """
    User model for storing user accounts.
    """
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)

    # Use timezone-aware UTC datetime for defaults
    created_at = db.Column(db.DateTime, default=lambda: datetime.datetime.now(datetime.timezone.utc))
    updated_at = db.Column(db.DateTime,
                           default=lambda: datetime.datetime.now(datetime.timezone.utc),
                           onupdate=lambda: datetime.datetime.now(datetime.timezone.utc))

    # Relationships (add later)
    # posts = db.relationship('Post', backref='author', lazy=True)
    # todos = db.relationship('Todo', backref='owner', lazy=True)

    def __init__(self, username, email, password):
        """Constructor for User model."""
        self.username = username
        self.email = email
        self.set_password(password)

    def set_password(self, password):
        """Hashes the provided password and stores it."""
        self.password_hash = bcrypt.generate_password_hash(password).decode('utf-8')

    def check_password(self, password):
        """Checks if the provided password matches the stored hash."""
        return bcrypt.check_password_hash(self.password_hash, password)

    def __repr__(self):
        """String representation of the User object."""
        return f'<User {self.username}>'
