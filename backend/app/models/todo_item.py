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
    user_id = db.Column(db.Integer, db.ForeignKey('users.id', ondelete='CASCADE'), nullable=False)

    title = db.Column(db.Text, nullable=False) # TEXT NOT NULL
    description = db.Column(db.Text, nullable=True) # TEXT, optional
    due_date = db.Column(db.Date, nullable=True) # DATE, optional

    status = db.Column(db.String(20), default='pending', nullable=False)
    priority = db.Column(db.String(20), default='medium', nullable=False)

    # New field to mark if the to-do item is a current focus
    is_current_focus = db.Column(db.Boolean, default=False, nullable=False)

    created_at = db.Column(db.DateTime, default=lambda: datetime.datetime.now(datetime.timezone.utc))
    updated_at = db.Column(db.DateTime,
                           default=lambda: datetime.datetime.now(datetime.timezone.utc),
                           onupdate=lambda: datetime.datetime.now(datetime.timezone.utc))
    completed_at = db.Column(db.DateTime, nullable=True)

    # user = db.relationship('User', backref=db.backref('todo_items', lazy=True))

    def __repr__(self):
        """String representation of the TodoItem object."""
        return f'<TodoItem {self.id}: {self.title[:30]}>'

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
            'is_current_focus': self.is_current_focus, # Include the new field
            'created_at': self.created_at.isoformat() + 'Z' if self.created_at else None,
            'updated_at': self.updated_at.isoformat() + 'Z' if self.updated_at else None,
            'completed_at': self.completed_at.isoformat() + 'Z' if self.completed_at else None
        }
