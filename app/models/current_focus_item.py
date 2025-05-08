# /your_project_root/app/models/current_focus_item.py
# Defines the CurrentFocusItem database model.

from ..extensions import db
import datetime

class CurrentFocusItem(db.Model):
    """
    CurrentFocusItem model for storing user's current activities, projects, or learning goals.
    Represents the "正在做什么" section of the Personal Anchor Overview.
    """
    __tablename__ = 'current_focus_items'

    id = db.Column(db.Integer, primary_key=True) # SERIAL PRIMARY KEY
    user_id = db.Column(db.Integer, db.ForeignKey('users.id', ondelete='CASCADE'), nullable=False)

    # Type of focus item, e.g., 'project', 'learning', 'challenge', 'role' etc.
    item_type = db.Column(db.String(50), nullable=True) # VARCHAR(50), consider making it NOT NULL if required

    title = db.Column(db.Text, nullable=False) # TEXT NOT NULL
    description = db.Column(db.Text, nullable=True) # TEXT
    start_date = db.Column(db.Date, nullable=True) # DATE, optional
    
    # Optional status field to track progress within the current focus
    status = db.Column(db.String(50), nullable=True) # VARCHAR(50), optional

    # Timestamps
    created_at = db.Column(db.DateTime, default=lambda: datetime.datetime.now(datetime.timezone.utc))
    updated_at = db.Column(db.DateTime,
                           default=lambda: datetime.datetime.now(datetime.timezone.utc),
                           onupdate=lambda: datetime.datetime.now(datetime.timezone.utc))

    # Relationship to User (optional)
    # user = db.relationship('User', backref=db.backref('current_focus_items', lazy='dynamic'))

    def __repr__(self):
        """String representation of the CurrentFocusItem object."""
        return f'<CurrentFocusItem {self.id}: {self.title[:30]}>'

    def to_dict(self):
        """Converts the CurrentFocusItem instance to a dictionary."""
        return {
            'id': self.id,
            'user_id': self.user_id,
            'item_type': self.item_type,
            'title': self.title,
            'description': self.description,
            'start_date': self.start_date.isoformat() if self.start_date else None,
            'status': self.status,
            'created_at': self.created_at.isoformat() + 'Z' if self.created_at else None,
            'updated_at': self.updated_at.isoformat() + 'Z' if self.updated_at else None,
        }
