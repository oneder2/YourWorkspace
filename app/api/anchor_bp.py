# /your_project_root/app/api/anchor_bp.py
# Blueprint for "Personal Anchor Overview" related API endpoints.

from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required, get_jwt_identity

# Import User model (which has the 'profile' relationship) and UserProfile model
from ..models.user import User
from ..models.user_profile import UserProfile
from ..extensions import db

# Create a Blueprint instance named 'anchor'
anchor_bp = Blueprint('anchor', __name__)

@anchor_bp.route('/ping', methods=['GET'])
def ping_anchor():
    """Simple test route to check if the anchor blueprint is registered."""
    return jsonify({"message": "Anchor API is alive!"}), 200

# --- User Profile Section ---

@anchor_bp.route('/profile', methods=['GET'])
@jwt_required()
def get_user_anchor_profile():
    """
    Retrieves the professional profile (title, bio) for the currently authenticated user.
    If a profile doesn't exist for an existing user (e.g., user created before profile feature),
    it creates an empty profile for them.
    """
    current_user_id_str = get_jwt_identity()
    try:
        current_user_id = int(current_user_id_str)
    except ValueError:
        return jsonify({"error": "Invalid user identity in token"}), 400

    user = db.session.get(User, current_user_id)

    if not user:
        return jsonify({"error": "User not found"}), 404

    if not user.profile:
        # Profile doesn't exist for this user, likely an older user.
        # Create one now.
        try:
            new_profile = UserProfile(id=user.id) # Associate with the current user's ID
            user.profile = new_profile # Link it to the user object
            # No need to db.session.add(new_profile) explicitly if user.profile assignment
            # and subsequent db.session.commit() handles the cascade correctly.
            # However, being explicit with add can be safer with some session configurations.
            db.session.add(new_profile)
            db.session.commit()
            print(f"INFO: Created missing profile for user_id: {user.id}") # For server logs
        except Exception as e:
            db.session.rollback()
            print(f"ERROR: Could not create missing profile for user_id {user.id}: {e}")
            return jsonify({"error": "Could not retrieve or create user profile."}), 500
        
        # After creating, user.profile should now be populated
        if not user.profile: # Should not happen if creation was successful
             return jsonify({"error": "Profile creation failed unexpectedly."}), 500


    return jsonify(user.profile.to_dict()), 200


@anchor_bp.route('/profile', methods=['PUT'])
@jwt_required()
def update_user_anchor_profile():
    """
    Updates the professional profile (title, bio) for the currently authenticated user.
    """
    current_user_id_str = get_jwt_identity()
    try:
        current_user_id = int(current_user_id_str)
    except ValueError:
        return jsonify({"error": "Invalid user identity in token"}), 400

    user = db.session.get(User, current_user_id)

    if not user:
        return jsonify({"error": "User not found"}), 404

    # Ensure user.profile exists (it should due to User.__init__ or GET /profile creating it)
    if not user.profile:
        # This is a fallback. In a robust system, you might create it here
        # if it somehow wasn't created, or log an error.
        # Given our User model and the GET endpoint, this should be less likely to be the first point of creation.
        print(f"INFO: Profile missing for user_id {user.id} during PUT, creating now.") # For server logs
        try:
            user.profile = UserProfile(id=user.id) # Create if missing
            db.session.add(user.profile)
            # A commit here might be too early if the subsequent updates fail.
            # It's generally better to commit once at the end of all operations.
        except Exception as e:
            db.session.rollback()
            print(f"ERROR: Could not create missing profile during PUT for user_id {user.id}: {e}")
            return jsonify({"error": "Could not initialize user profile for update."}), 500


    data = request.get_json()
    if not data:
        return jsonify({"error": "Request body must be JSON and cannot be empty"}), 400

    updated = False # Flag to check if any actual update happened

    if 'professional_title' in data:
        title = data['professional_title']
        if title is not None and not isinstance(title, str):
            return jsonify({"error": "professional_title must be a string or null"}), 400
        user.profile.professional_title = title
        updated = True

    if 'one_liner_bio' in data:
        bio = data['one_liner_bio']
        if bio is not None and not isinstance(bio, str):
            return jsonify({"error": "one_liner_bio must be a string or null"}), 400
        user.profile.one_liner_bio = bio
        updated = True

    if not updated and data:
        return jsonify({"message": "No relevant profile fields provided for update."}), 200


    try:
        db.session.commit() # Commit all changes (profile creation if any, and updates)
        return jsonify(user.profile.to_dict()), 200
    except Exception as e:
        db.session.rollback()
        print(f"Error updating user profile: {e}")
        return jsonify({"error": "An unexpected error occurred while updating the profile."}), 500

# Endpoints for Achievements, Current Focus, Future Plans will be added later.