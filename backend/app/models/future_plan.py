# /your_project_root/app/models/future_plan.py
# Defines the FuturePlan database model.

from ..extensions import db
import datetime
from .base import BaseModel
from typing import Dict, Any, Optional

class FuturePlan(BaseModel):
    """
    FuturePlan model for storing user's future goals, plans, or vision items.
    Represents the "打算做什么" section of the Personal Anchor Overview.
    Inherits common fields and methods from BaseModel.
    """
    __tablename__ = 'future_plans'

    id = db.Column(db.Integer, primary_key=True) # SERIAL PRIMARY KEY
    user_id = db.Column(db.Integer, db.ForeignKey('users.id', ondelete='CASCADE'), nullable=False)

    # Type of goal, e.g., 'short_term_goal', 'long_term_vision', 'skill_development'
    goal_type = db.Column(db.String(50), nullable=True) # VARCHAR(50), consider making NOT NULL if required

    title = db.Column(db.Text, nullable=False) # TEXT NOT NULL
    description = db.Column(db.Text, nullable=False) # TEXT NOT NULL
    target_date = db.Column(db.Date, nullable=True) # DATE, optional

    # Status of the plan
    # Allowed values: 'active', 'achieved', 'deferred', 'abandoned'
    # Default: 'active'
    status = db.Column(db.String(20), default='active', nullable=False)

    # Relationship to User (optional)
    # user = db.relationship('User', backref=db.backref('future_plans', lazy='dynamic'))

    # Database constraints for status (CHECK constraint can be added via migration)
    # CHECK (status IN ('active', 'achieved', 'deferred', 'abandoned'))

    def __repr__(self) -> str:
        """String representation of the FuturePlan object."""
        return f'<FuturePlan {self.id}: {self.title[:30]}>'

    def to_dict(self) -> Dict[str, Any]:
        """Converts the FuturePlan instance to a dictionary."""
        return {
            'id': self.id,
            'user_id': self.user_id,
            'goal_type': self.goal_type,
            'title': self.title,
            'description': self.description,
            'target_date': self.format_date(self.target_date),
            'status': self.status,
            'created_at': self.format_datetime(self.created_at),
            'updated_at': self.format_datetime(self.updated_at),
        }
