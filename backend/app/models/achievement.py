# /your_project_root/app/models/achievement.py
# Defines the Achievement database model.

from ..extensions import db
import datetime

class Achievement(db.Model):
    """
    Achievement model for storing user's past accomplishments.
    """
    __tablename__ = 'achievements'

    id = db.Column(db.Integer, primary_key=True) # SERIAL PRIMARY KEY
    user_id = db.Column(db.Integer, db.ForeignKey('users.id', ondelete='CASCADE'), nullable=False)

    title = db.Column(db.Text, nullable=False) # TEXT NOT NULL
    description = db.Column(db.Text, nullable=True) # TEXT
    quantifiable_results = db.Column(db.Text, nullable=True) # TEXT, optional
    
    # For storing a list of skills. JSONB is PostgreSQL-specific.
    # For broader compatibility, db.JSON can be used, but JSONB offers better performance and indexing in PostgreSQL.
    core_skills_json = db.Column(db.JSON, nullable=True) # JSONB in PostgreSQL, stores e.g., ["Python", "Flask", "Project Management"]

    date_achieved = db.Column(db.Date, nullable=True) # DATE, optional

    # Timestamps
    created_at = db.Column(db.DateTime, default=lambda: datetime.datetime.now(datetime.timezone.utc))
    updated_at = db.Column(db.DateTime,
                           default=lambda: datetime.datetime.now(datetime.timezone.utc),
                           onupdate=lambda: datetime.datetime.now(datetime.timezone.utc))

    # Relationship to User (optional, if you need to access user from achievement instance directly)
    # user = db.relationship('User', backref=db.backref('achievements', lazy='dynamic'))

    def __repr__(self):
        """String representation of the Achievement object."""
        return f'<Achievement {self.id}: {self.title[:30]}>'

    def to_dict(self):
        """Converts the Achievement instance to a dictionary."""
        return {
            'id': self.id,
            'user_id': self.user_id,
            'title': self.title,
            'description': self.description,
            'quantifiable_results': self.quantifiable_results,
            'core_skills_json': self.core_skills_json if self.core_skills_json else [], # Default to empty list if null
            'date_achieved': self.date_achieved.isoformat() if self.date_achieved else None,
            'created_at': self.created_at.isoformat() + 'Z' if self.created_at else None,
            'updated_at': self.updated_at.isoformat() + 'Z' if self.updated_at else None,
        }
