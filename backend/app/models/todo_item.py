# /your_project_root/app/models/todo_item.py
# Defines the TodoItem database model.

from ..extensions import db
import datetime

class TodoItem(db.Model):
    """
    TodoItem model for storing individual to-do tasks.
    """
    __tablename__ = 'todo_items'

    id = db.Column(db.Integer, primary_key=True) # SERIAL PRIMARY KEY
    user_id = db.Column(db.Integer, db.ForeignKey('users.id', ondelete='CASCADE'), nullable=False) # Foreign key to users table

    title = db.Column(db.Text, nullable=False) # TEXT NOT NULL
    description = db.Column(db.Text, nullable=True) # TEXT, optional
    due_date = db.Column(db.Date, nullable=True) # DATE, optional

    # Status of the to-do item
    # Allowed values: 'pending', 'in_progress', 'completed', 'deferred'
    # Default: 'pending'
    status = db.Column(db.String(20), default='pending', nullable=False)

    # Priority of the to-do item
    # Allowed values: 'low', 'medium', 'high'
    # Default: 'medium'
    priority = db.Column(db.String(20), default='medium', nullable=False)

    # Timestamps
    # default=lambda: datetime.datetime.now(datetime.timezone.utc) ensures timezone-aware UTC timestamps
    created_at = db.Column(db.DateTime, default=lambda: datetime.datetime.now(datetime.timezone.utc))
    updated_at = db.Column(db.DateTime,
                           default=lambda: datetime.datetime.now(datetime.timezone.utc),
                           onupdate=lambda: datetime.datetime.now(datetime.timezone.utc))
    completed_at = db.Column(db.DateTime, nullable=True) # TIMESTAMP, nullable, records when the task was completed

    # Define relationship to User model (optional, but good for ORM access)
    # user = db.relationship('User', backref=db.backref('todo_items', lazy=True)) # Example if you need to access user from todo or todos from user

    # Database constraints for status and priority (handled by CHECK constraints in raw SQL if needed,
    # or can be enforced at the application level. SQLAlchemy doesn't natively create CHECK constraints
    # for all database backends in a simple way, but enums or explicit checks in routes are common).
    # For PostgreSQL, you could add these via migrations:
    # CHECK (status IN ('pending', 'in_progress', 'completed', 'deferred'))
    # CHECK (priority IN ('low', 'medium', 'high'))

    def __repr__(self):
        """String representation of the TodoItem object."""
        return f'<TodoItem {self.id}: {self.title[:30]}>'

    # --- Serialization (to dictionary) ---
    # This method can be used to easily convert model instances to JSON-friendly dictionaries.
    def to_dict(self):
        """Converts the TodoItem instance to a dictionary."""
        return {
            'id': self.id,
            'user_id': self.user_id,
            'title': self.title,
            'description': self.description,
            'due_date': self.due_date.isoformat() if self.due_date else None,
            'status': self.status,
            'priority': self.priority,
            'created_at': self.created_at.isoformat() + 'Z' if self.created_at else None,
            'updated_at': self.updated_at.isoformat() + 'Z' if self.updated_at else None,
            'completed_at': self.completed_at.isoformat() + 'Z' if self.completed_at else None
        }
