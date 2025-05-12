# /your_project_root/app/api/anchor_bp.py
# Blueprint for "Personal Anchor Overview" (User Profile) related API endpoints.

from flask import Blueprint, jsonify, request, current_app
from flask_jwt_extended import jwt_required, get_jwt_identity
import datetime # Keep for potential future use in profile, though not directly used now

# Import models
from ..models.user import User
from ..models.user_profile import UserProfile
# Achievement and FuturePlan models are no longer directly managed here
from ..extensions import db

# Create a Blueprint instance named 'anchor'
anchor_bp = Blueprint('anchor', __name__)

@anchor_bp.route('/ping', methods=['GET'])
def ping_anchor():
    """Simple test route to check if the anchor blueprint is registered."""
    return jsonify({"message": "Anchor (Profile) API is alive!"}), 200

# --- User Profile Section ---
@anchor_bp.route('/profile', methods=['GET'])
@jwt_required()
def get_user_anchor_profile():
    current_user_id_str = get_jwt_identity()
    try:
        current_user_id = int(current_user_id_str)
    except ValueError:
        return jsonify({"error": "Invalid user identity in token"}), 400
    
    user = db.session.get(User, current_user_id)
    if not user:
        return jsonify({"error": "User not found"}), 404
    
    if not user.profile:
        try:
            # Automatically create a profile if it doesn't exist for the user
            new_profile = UserProfile(id=user.id) # Assuming UserProfile.id is ForeignKey to User.id
            user.profile = new_profile # Associate with the user
            db.session.add(new_profile)
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            current_app.logger.error(f"Could not create user profile on GET: {e}", exc_info=True)
            return jsonify({"error": "Could not retrieve or create user profile."}), 500
            
    return jsonify(user.profile.to_dict()), 200


@anchor_bp.route('/profile', methods=['PUT'])
@jwt_required()
def update_user_anchor_profile():
    current_user_id_str = get_jwt_identity()
    try:
        current_user_id = int(current_user_id_str)
    except ValueError:
        return jsonify({"error": "Invalid user identity in token"}), 400

    user = db.session.get(User, current_user_id)
    if not user:
        return jsonify({"error": "User not found"}), 404

    if not user.profile: # Should be auto-created by GET, but as a fallback or if GET was never called
        try:
            user.profile = UserProfile(id=user.id)
            db.session.add(user.profile)
            # We might not commit here, let the subsequent updates be part of the same transaction
        except Exception as e:
            db.session.rollback() # Rollback if profile creation itself failed
            current_app.logger.error(f"Could not initialize user profile for update: {e}", exc_info=True)
            return jsonify({"error": "Could not initialize user profile for update."}), 500

    data = request.get_json()
    if not data: 
        return jsonify({"error": "Request body must be JSON and cannot be empty"}), 400

    updated_fields_count = 0

    # Fields that can be updated in the UserProfile
    profile_fields = ['professional_title', 'one_liner_bio', 'skill', 'summary']

    for field_name in profile_fields:
        if field_name in data:
            field_value = data[field_name]
            # Add specific validation if needed, e.g., length, type
            if field_value is not None and not isinstance(field_value, str):
                 return jsonify({"error": f"{field_name} must be a string or null"}), 400
            setattr(user.profile, field_name, field_value)
            updated_fields_count += 1
    
    if updated_fields_count == 0 and data: 
         return jsonify({"message": "No relevant profile fields provided for update."}), 200 # Or 400 if this is an error

    try:
        db.session.commit()
        return jsonify(user.profile.to_dict()), 200
    except Exception as e:
        db.session.rollback()
        current_app.logger.error(f"Error updating user profile: {e}", exc_info=True)
        return jsonify({"error": "An unexpected error occurred while updating the profile."}), 500
    