# /your_project_root/app/api/achievements_bp.py
# Blueprint for "Achievements" (Done) related API endpoints.

from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required, get_jwt_identity
import datetime

# Import models and db instance
from ..models.user import User # Assuming User model might be needed for context, though not directly used in these routes
from ..models.achievement import Achievement
from ..extensions import db

# Create a Blueprint instance named 'achievements'
achievements_bp = Blueprint('achievements', __name__)

@achievements_bp.route('/ping', methods=['GET'])
def ping_achievements():
    """Simple test route to check if the achievements blueprint is registered."""
    return jsonify({"message": "Achievements API is alive!"}), 200

# --- Achievements Section ("做过什么") ---
@achievements_bp.route('/', methods=['POST']) # Changed from '/achievements' to '/'
@jwt_required()
def create_achievement():
    current_user_id_str = get_jwt_identity()
    try:
        current_user_id = int(current_user_id_str)
    except ValueError:
        return jsonify({"error": "Invalid user identity in token"}), 400

    data = request.get_json()
    if not data:
        return jsonify({"error": "Request body must be JSON"}), 400

    title = data.get('title')
    if not title or not isinstance(title, str) or not title.strip():
        return jsonify({"error": "Title is required and must be a non-empty string"}), 400

    description = data.get('description')
    if description is not None and not isinstance(description, str):
        return jsonify({"error": "Description must be a string if provided"}), 400

    quantifiable_results = data.get('quantifiable_results')
    if quantifiable_results is not None and not isinstance(quantifiable_results, str):
        return jsonify({"error": "Quantifiable results must be a string if provided"}), 400

    core_skills_json_input = data.get('core_skills_json')
    validated_skills = [] # Default to empty list
    if core_skills_json_input is not None:
        if not isinstance(core_skills_json_input, list):
            return jsonify({"error": "core_skills_json must be a list if provided"}), 400
        for skill_item in core_skills_json_input:
            if not isinstance(skill_item, str):
                return jsonify({"error": "All items in core_skills_json must be strings"}), 400
        validated_skills = core_skills_json_input

    date_achieved_str = data.get('date_achieved')
    date_achieved_obj = None
    if date_achieved_str:
        try:
            date_achieved_obj = datetime.datetime.strptime(date_achieved_str, '%Y-%m-%d').date()
        except ValueError:
            return jsonify({"error": "Invalid date_achieved format. Please use YYYY-MM-DD."}), 400

    try:
        new_achievement = Achievement(
            user_id=current_user_id,
            title=title.strip(),
            description=description.strip() if description else None,
            quantifiable_results=quantifiable_results.strip() if quantifiable_results else None,
            core_skills_json=validated_skills,
            date_achieved=date_achieved_obj
        )
        db.session.add(new_achievement)
        db.session.commit()
        return jsonify(new_achievement.to_dict()), 201
    except Exception as e:
        db.session.rollback()
        # current_app.logger.error(f"Error creating achievement: {e}", exc_info=True) # Use current_app.logger
        return jsonify({"error": "An unexpected error occurred while creating the achievement."}), 500

@achievements_bp.route('/', methods=['GET']) # Changed from '/achievements' to '/'
@jwt_required()
def get_all_achievements():
    current_user_id_str = get_jwt_identity()
    try: current_user_id = int(current_user_id_str)
    except ValueError: return jsonify({"error": "Invalid user identity in token"}), 400
    user_achievements = Achievement.query.filter_by(user_id=current_user_id)\
        .order_by(Achievement.date_achieved.desc().nullslast(), Achievement.created_at.desc())\
        .all()
    return jsonify([ach.to_dict() for ach in user_achievements]), 200

@achievements_bp.route('/<int:achievement_id>', methods=['GET']) # Changed from '/achievements/<id>' to '/<id>'
@jwt_required()
def get_achievement_by_id(achievement_id):
    current_user_id_str = get_jwt_identity()
    try: current_user_id = int(current_user_id_str)
    except ValueError: return jsonify({"error": "Invalid user identity in token"}), 400
    achievement = db.session.get(Achievement, achievement_id)
    if not achievement: return jsonify({"error": "Achievement not found"}), 404
    if achievement.user_id != current_user_id: return jsonify({"error": "Forbidden: You do not have permission to access this achievement"}), 403
    return jsonify(achievement.to_dict()), 200

@achievements_bp.route('/<int:achievement_id>', methods=['PUT']) # Changed from '/achievements/<id>' to '/<id>'
@jwt_required()
def update_achievement(achievement_id):
    current_user_id_str = get_jwt_identity()
    try: current_user_id = int(current_user_id_str)
    except ValueError: return jsonify({"error": "Invalid user identity in token"}), 400
    achievement = db.session.get(Achievement, achievement_id)
    if not achievement: return jsonify({"error": "Achievement not found"}), 404
    if achievement.user_id != current_user_id: return jsonify({"error": "Forbidden: You do not have permission to update this achievement"}), 403
    data = request.get_json()
    if not data: return jsonify({"error": "Request body must be JSON and cannot be empty"}), 400

    updated_fields_count = 0

    if 'title' in data:
        title = data['title']
        if not title or not isinstance(title, str) or not title.strip():
            return jsonify({"error": "Title is required and must be a non-empty string"}), 400
        achievement.title = title.strip()
        updated_fields_count += 1
    if 'description' in data:
        description = data['description']
        if description is not None and not isinstance(description, str):
            return jsonify({"error": "Description must be a string if provided"}), 400
        achievement.description = description.strip() if description else None
        updated_fields_count += 1
    if 'quantifiable_results' in data:
        quantifiable_results = data['quantifiable_results']
        if quantifiable_results is not None and not isinstance(quantifiable_results, str):
            return jsonify({"error": "Quantifiable results must be a string if provided"}), 400
        achievement.quantifiable_results = quantifiable_results.strip() if quantifiable_results else None
        updated_fields_count += 1
    if 'core_skills_json' in data:
        core_skills_json_input = data['core_skills_json']
        if core_skills_json_input is not None:
            if not isinstance(core_skills_json_input, list):
                return jsonify({"error": "core_skills_json must be a list if provided"}), 400
            for skill_item in core_skills_json_input:
                if not isinstance(skill_item, str):
                    return jsonify({"error": "All items in core_skills_json must be strings"}), 400
            achievement.core_skills_json = core_skills_json_input
        else:
             achievement.core_skills_json = None
        updated_fields_count += 1
    if 'date_achieved' in data:
        date_achieved_str = data['date_achieved']
        if date_achieved_str is None:
             achievement.date_achieved = None
        elif isinstance(date_achieved_str, str):
            try:
                achievement.date_achieved = datetime.datetime.strptime(date_achieved_str, '%Y-%m-%d').date()
            except ValueError:
                return jsonify({"error": "Invalid date_achieved format. Please use YYYY-MM-DD or null."}), 400
        else:
             return jsonify({"error": "date_achieved must be a string in YYYY-MM-DD format or null."}), 400
        updated_fields_count += 1

    if updated_fields_count == 0 and data:
        return jsonify({"message": "No relevant achievement fields provided for update."}), 200
    try:
        db.session.commit()
        return jsonify(achievement.to_dict()), 200
    except Exception as e:
        db.session.rollback()
        # current_app.logger.error(f"Error updating achievement: {e}", exc_info=True) # Use current_app.logger
        return jsonify({"error": "An unexpected error occurred while updating the achievement."}), 500

@achievements_bp.route('/<int:achievement_id>', methods=['DELETE']) # Changed from '/achievements/<id>' to '/<id>'
@jwt_required()
def delete_achievement(achievement_id):
    current_user_id_str = get_jwt_identity()
    try: current_user_id = int(current_user_id_str)
    except ValueError: return jsonify({"error": "Invalid user identity in token"}), 400
    achievement = db.session.get(Achievement, achievement_id)
    if not achievement: return jsonify({"error": "Achievement not found"}), 404
    if achievement.user_id != current_user_id: return jsonify({"error": "Forbidden"}), 403
    try:
        db.session.delete(achievement)
        db.session.commit()
        return '', 204
    except Exception as e:
        db.session.rollback()
        # current_app.logger.error(f"Error deleting achievement: {e}", exc_info=True) # Use current_app.logger
        return jsonify({"error": "Error deleting achievement."}), 500
