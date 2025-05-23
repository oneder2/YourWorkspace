# /your_project_root/app/utils/request_validation.py
# Utilities for validating request data.

from flask import request, jsonify
from typing import Dict, Any, Optional, Tuple, Union, List, Callable
import functools
from .api_responses import api_validation_error

def validate_json_request(required_fields: Optional[List[str]] = None) -> Callable:
    """
    Decorator to validate that a request has JSON data and required fields.
    
    Args:
        required_fields: List of field names that must be present in the JSON data
        
    Returns:
        Decorated function
    """
    def decorator(f: Callable) -> Callable:
        @functools.wraps(f)
        def decorated_function(*args, **kwargs):
            # Check if request has JSON data
            if not request.is_json:
                return jsonify({"error": "Request body must be JSON"}), 400
            
            data = request.get_json()
            
            # Check for required fields
            if required_fields:
                missing_fields = [field for field in required_fields if field not in data or data[field] is None]
                if missing_fields:
                    return api_validation_error(
                        {field: ["This field is required"] for field in missing_fields},
                        message=f"Missing required fields: {', '.join(missing_fields)}"
                    )
            
            return f(*args, **kwargs)
        return decorated_function
    return decorator

def validate_field_type(data: Dict[str, Any], field: str, expected_type: type, allow_none: bool = True) -> Optional[str]:
    """
    Validate that a field in the data is of the expected type.
    
    Args:
        data: The data dictionary
        field: The field name to validate
        expected_type: The expected type
        allow_none: Whether None is an acceptable value
        
    Returns:
        Error message if validation fails, None otherwise
    """
    if field not in data:
        return None
    
    value = data[field]
    
    if value is None:
        if allow_none:
            return None
        return f"{field} cannot be null"
    
    if not isinstance(value, expected_type):
        return f"{field} must be of type {expected_type.__name__}"
    
    return None

def validate_enum_field(data: Dict[str, Any], field: str, allowed_values: List[str], allow_none: bool = True) -> Optional[str]:
    """
    Validate that a field in the data is one of the allowed values.
    
    Args:
        data: The data dictionary
        field: The field name to validate
        allowed_values: List of allowed values
        allow_none: Whether None is an acceptable value
        
    Returns:
        Error message if validation fails, None otherwise
    """
    if field not in data:
        return None
    
    value = data[field]
    
    if value is None:
        if allow_none:
            return None
        return f"{field} cannot be null"
    
    if value not in allowed_values:
        return f"{field} must be one of: {', '.join(allowed_values)}"
    
    return None
