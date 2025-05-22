# /your_project_root/app/models/base.py
# Base model class with common functionality for all models.

from ..extensions import db
import datetime
from typing import Dict, Any, Optional, Union, List

class BaseModel(db.Model):
    """
    Abstract base model with common functionality.
    All models should inherit from this class to ensure consistent behavior.
    """
    __abstract__ = True
    
    # Common timestamp fields
    created_at = db.Column(db.DateTime, default=lambda: datetime.datetime.now(datetime.timezone.utc))
    updated_at = db.Column(db.DateTime,
                          default=lambda: datetime.datetime.now(datetime.timezone.utc),
                          onupdate=lambda: datetime.datetime.now(datetime.timezone.utc))
    
    def to_dict(self) -> Dict[str, Any]:
        """
        Base implementation of to_dict - override in subclasses.
        This method should convert model instances to dictionaries for API responses.
        """
        raise NotImplementedError("Subclasses must implement to_dict()")
    
    @staticmethod
    def format_datetime(dt: Optional[datetime.datetime]) -> Optional[str]:
        """
        Format a datetime object to ISO 8601 string with Z suffix for UTC.
        
        Args:
            dt: The datetime object to format
            
        Returns:
            Formatted datetime string or None if dt is None
        """
        if dt is None:
            return None
        return dt.isoformat() + 'Z'
    
    @staticmethod
    def format_date(date: Optional[datetime.date]) -> Optional[str]:
        """
        Format a date object to ISO format (YYYY-MM-DD).
        
        Args:
            date: The date object to format
            
        Returns:
            Formatted date string or None if date is None
        """
        if date is None:
            return None
        return date.isoformat()
