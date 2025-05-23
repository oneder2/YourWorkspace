# /your_project_root/app/utils/api_responses.py
# Standardized API response utilities.

from flask import jsonify
from typing import Dict, Any, Optional, Tuple, Union, List

def api_success(
    data: Any = None, 
    message: Optional[str] = None, 
    status_code: int = 200, 
    meta: Optional[Dict[str, Any]] = None
) -> Tuple[Dict[str, Any], int]:
    """
    Standardized API success response generator.
    
    Args:
        data: The main response data
        message: A success message
        status_code: HTTP status code
        meta: Metadata like pagination info
        
    Returns:
        tuple: (JSON response, status code)
    """
    response = {}
    
    if data is not None:
        response["data"] = data
        
    if message:
        response["message"] = message
        
    if meta:
        response["meta"] = meta
        
    return jsonify(response), status_code

def api_error(
    message: str, 
    status_code: int = 400, 
    details: Optional[Dict[str, Any]] = None,
    error_code: Optional[str] = None
) -> Tuple[Dict[str, Any], int]:
    """
    Standardized API error response generator.
    
    Args:
        message: Main error message
        status_code: HTTP status code
        details: Additional error details
        error_code: Optional error code for client-side error handling
        
    Returns:
        tuple: (JSON response, status code)
    """
    response = {
        "error": message
    }
    
    if details:
        response["details"] = details
    
    if error_code:
        response["error_code"] = error_code
        
    return jsonify(response), status_code

def api_validation_error(
    errors: Dict[str, List[str]], 
    message: str = "Validation error", 
    status_code: int = 400
) -> Tuple[Dict[str, Any], int]:
    """
    Specialized error response for validation errors.
    
    Args:
        errors: Dictionary of field names to error messages
        message: Main error message
        status_code: HTTP status code
        
    Returns:
        tuple: (JSON response, status code)
    """
    return api_error(
        message=message,
        status_code=status_code,
        details={"validation_errors": errors},
        error_code="VALIDATION_ERROR"
    )
