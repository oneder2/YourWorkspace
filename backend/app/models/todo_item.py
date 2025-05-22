# /your_project_root/app/models/todo_item.py
# Defines the TodoItem database model.

from ..extensions import db
import datetime
from .base import BaseModel
from typing import Dict, Any

class TodoItem(BaseModel):
    """
    TodoItem model for storing individual to-do tasks.
    Inherits common fields and methods from BaseModel.
    """
    __tablename__ = 'todo_items'

    id = db.Column(db.Integer, primary_key=True) # SERIAL PRIMARY KEY
    user_id = db.Column(db.Integer, db.ForeignKey('users.id', ondelete='CASCADE'), nullable=False)

    title = db.Column(db.Text, nullable=False) # TEXT NOT NULL
    description = db.Column(db.Text, nullable=True) # TEXT, optional
    due_date = db.Column(db.Date, nullable=True) # DATE, optional

    status = db.Column(db.String(20), default='pending', nullable=False)
    priority = db.Column(db.String(20), default='medium', nullable=False)

    # Field to mark if the to-do item is a current focus
    is_current_focus = db.Column(db.Boolean, default=False, nullable=False)

    # completed_at is specific to TodoItem, not in BaseModel
    completed_at = db.Column(db.DateTime, nullable=True)

    # user = db.relationship('User', backref=db.backref('todo_items', lazy=True))

    def __repr__(self) -> str:
        """String representation of the TodoItem object."""
        return f'<TodoItem {self.id}: {self.title[:30]}>'

    def to_dict(self) -> Dict[str, Any]:
        """Converts the TodoItem instance to a dictionary."""
        return {
            'id': self.id,
            'user_id': self.user_id,
            'title': self.title,
            'description': self.description,
            'due_date': self.format_date(self.due_date),
            'status': self.status,
            'priority': self.priority,
            'is_current_focus': self.is_current_focus,
            'created_at': self.format_datetime(self.created_at),
            'updated_at': self.format_datetime(self.updated_at),
            'completed_at': self.format_datetime(self.completed_at)
        }
