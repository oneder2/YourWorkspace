# /your_project_root/app/models/token_blocklist.py
# Defines the TokenBlocklist model for storing revoked JWTs.

from ..extensions import db
import datetime # Import datetime module

class TokenBlocklist(db.Model):
    """
    Model for storing JTI of revoked JWTs.
    """
    __tablename__ = 'token_blocklist'

    id = db.Column(db.Integer, primary_key=True)
    jti = db.Column(db.String(36), nullable=False, unique=True, index=True)
    token_type = db.Column(db.String(10), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    
    # Use timezone-aware UTC datetime for default
    created_at = db.Column(db.DateTime, nullable=False,
                           default=lambda: datetime.datetime.now(datetime.timezone.utc))

    user = db.relationship('User')

    def __repr__(self):
        return f"<TokenBlocklist jti={self.jti}, user_id={self.user_id}>"
