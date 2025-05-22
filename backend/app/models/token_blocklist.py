# /your_project_root/app/models/token_blocklist.py
# Defines the TokenBlocklist model for storing revoked JWTs.

from ..extensions import db
import datetime
from .base import BaseModel
from typing import Dict, Any

class TokenBlocklist(BaseModel):
    """
    Model for storing JTI of revoked JWTs.
    Inherits common fields and methods from BaseModel.
    """
    __tablename__ = 'token_blocklist'

    id = db.Column(db.Integer, primary_key=True)
    jti = db.Column(db.String(36), nullable=False, unique=True, index=True)
    token_type = db.Column(db.String(10), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)

    # No need for updated_at in this model, so we'll override it to None
    updated_at = None

    user = db.relationship('User')

    def __repr__(self) -> str:
        """String representation of the TokenBlocklist object."""
        return f"<TokenBlocklist jti={self.jti}, user_id={self.user_id}>"

    def to_dict(self) -> Dict[str, Any]:
        """Converts the TokenBlocklist instance to a dictionary."""
        return {
            'id': self.id,
            'jti': self.jti,
            'token_type': self.token_type,
            'user_id': self.user_id,
            'created_at': self.format_datetime(self.created_at),
        }
