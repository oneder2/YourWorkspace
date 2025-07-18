# /your_project_root/app/models/user_profile.py
# Defines the UserProfile database model.

from ..extensions import db
import datetime
from .base import BaseModel
from typing import Dict, Any, Optional

class UserProfile(BaseModel):
    """
    UserProfile model for storing additional user profile information,
    including professional title and one-liner bio for the "Anchor Overview".
    This model has a one-to-one relationship with the User model.
    Inherits common fields and methods from BaseModel.
    """
    __tablename__ = 'user_profiles'

    # The id will be a foreign key to users.id and also the primary key for this table.
    # This enforces the one-to-one relationship.
    id = db.Column(db.Integer, db.ForeignKey('users.id', ondelete='CASCADE'), primary_key=True)

    professional_title = db.Column(db.String(255), nullable=True) # VARCHAR(255)
    one_liner_bio = db.Column(db.Text, nullable=True) # TEXT
    skill = db.Column(db.Text, nullable=True) # TEXT - New field for user skills
    summary = db.Column(db.Text, nullable=True) # TEXT - New field for user summary

    # --- Relationship to User ---
    # This creates a bidirectional relationship:
    # - UserProfile instance will have a 'user' attribute to access the parent User.
    # - User instance will have a 'profile' attribute to access this UserProfile.
    # 'uselist=False' signifies a one-to-one relationship from the User's perspective.
    # 'back_populates' is preferred over 'backref' for explicit relationship definition.
    user = db.relationship('User', back_populates='profile')

    def __repr__(self) -> str:
        """String representation of the UserProfile object."""
        return f'<UserProfile for UserID {self.id}>'

    def to_dict(self) -> Dict[str, Any]:
        """Converts the UserProfile instance to a dictionary."""
        return {
            'user_id': self.id, # Same as user.id
            'professional_title': self.professional_title,
            'one_liner_bio': self.one_liner_bio,
            'skill': self.skill,
            'summary': self.summary,
            'created_at': self.format_datetime(self.created_at),
            'updated_at': self.format_datetime(self.updated_at),
        }
