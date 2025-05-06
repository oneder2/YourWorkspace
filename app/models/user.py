# /your_project_root/app/models/user.py
# Defines the User database model.

from ..extensions import db, bcrypt
import datetime

class User(db.Model):
    """
    User model for storing user accounts.
    """
    # Explicitly specify the table name
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False) # Store hashed password
    created_at = db.Column(db.DateTime, default=datetime.datetime.now("UTC"))
    updated_at = db.Column(db.DateTime, default=datetime.datetime.now("UTC"), onupdate=datetime.datetime.now("UTC"))

    # Relationships (add later)
    # posts = db.relationship('Post', backref='author', lazy=True)
    # todos = db.relationship('Todo', backref='owner', lazy=True)

    def __init__(self, username, email, password):
        """Constructor for User model."""
        self.username = username
        self.email = email
        self.set_password(password) # Hash password on creation

    def set_password(self, password):
        """Hashes the provided password and stores it."""
        # Generate a salt and hash the password using bcrypt
        self.password_hash = bcrypt.generate_password_hash(password).decode('utf-8')

    def check_password(self, password):
        """Checks if the provided password matches the stored hash."""
        # Use bcrypt to compare the provided password with the stored hash
        return bcrypt.check_password_hash(self.password_hash, password)

    def __repr__(self):
        """String representation of the User object."""
        return f'<User {self.username}>'

    # Add methods for serialization (to dict/JSON) later if not using Marshmallow
    # def to_dict(self):
    #     return {
    #         'id': self.id,
    #         'username': self.username,
    #         'email': self.email,
    #         'created_at': self.created_at.isoformat() + 'Z',
    #         'updated_at': self.updated_at.isoformat() + 'Z'
    #         # DO NOT include password_hash
    #     }
