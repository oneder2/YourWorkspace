# /your_project_root/app/api/anchor_bp.py
# Blueprint for "Personal Anchor Overview" related API endpoints.

from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required, get_jwt_identity
import datetime

# Import models
from ..models.user import User
from ..models.user_profile import UserProfile
from ..models.achievement import Achievement
# Removed import of CurrentFocusItem as it's no longer needed
from ..models.future_plan import FuturePlan
from ..extensions import db

# Create a Blueprint instance named 'anchor'
anchor_bp = Blueprint('anchor', __name__)

# Allowed values for FuturePlan status - for validation
ALLOWED_FUTURE_PLAN_STATUSES = ['active', 'achieved', 'deferred', 'abandoned']


@anchor_bp.route('/ping', methods=['GET'])
def ping_anchor():
    """Simple test route to check if the anchor blueprint is registered."""
    return jsonify({"message": "Anchor API is alive!"}), 200

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
            new_profile = UserProfile(id=user.id)
            user.profile = new_profile
            db.session.add(new_profile)
            db.session.commit()
        except Exception as e:
            db.session.rollback()
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

    if not user.profile: # Should be auto-created, but as a fallback
        try:
            user.profile = UserProfile(id=user.id)
            db.session.add(user.profile)
        except Exception as e:
            db.session.rollback()
            return jsonify({"error": "Could not initialize user profile for update."}), 500

    data = request.get_json()
    if not data: # Handles {} as well, as an empty dict is falsy
        return jsonify({"error": "Request body must be JSON and cannot be empty"}), 400

    updated_fields_count = 0

    if 'professional_title' in data:
        title_val = data['professional_title']
        if title_val is not None and not isinstance(title_val, str):
            return jsonify({"error": "professional_title must be a string or null"}), 400
        user.profile.professional_title = title_val
        updated_fields_count += 1

    if 'one_liner_bio' in data:
        bio_val = data['one_liner_bio']
        if bio_val is not None and not isinstance(bio_val, str):
            return jsonify({"error": "one_liner_bio must be a string or null"}), 400
        user.profile.one_liner_bio = bio_val
        updated_fields_count += 1

    if 'skill' in data:
        skill_val = data['skill']
        if skill_val is not None and not isinstance(skill_val, str):
            return jsonify({"error": "skill must be a string or null"}), 400
        user.profile.skill = skill_val
        updated_fields_count += 1

    if 'summary' in data:
        summary_val = data['summary']
        if summary_val is not None and not isinstance(summary_val, str):
            return jsonify({"error": "summary must be a string or null"}), 400
        user.profile.summary = summary_val
        updated_fields_count += 1

    # Check if any known fields were actually in the payload.
    # This prevents a 200 OK for a payload like {"unknown_field": "value"}
    # Or more simply, if data was provided but no valid fields were updated:
    if updated_fields_count == 0 and data: # data is not empty, but no valid fields were processed
         return jsonify({"message": "No relevant profile fields provided for update."}), 200


    try:
        db.session.commit()
        return jsonify(user.profile.to_dict()), 200
    except Exception as e:
        db.session.rollback()
        print(f"Error updating user profile: {e}")
        return jsonify({"error": "An unexpected error occurred while updating the profile."}), 500

# --- Achievements Section ("做过什么") ---
@anchor_bp.route('/achievements', methods=['POST'])
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
            return jsonify({"error": "core_skills_json must be a list if provided"}), 400 # Check if it's a list first
        for skill_item in core_skills_json_input: # Then check items in the list
            if not isinstance(skill_item, str):
                return jsonify({"error": "All items in core_skills_json must be strings"}), 400
        validated_skills = core_skills_json_input # If all checks pass

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
            core_skills_json=validated_skills, # Use the validated list
            date_achieved=date_achieved_obj
        )
        db.session.add(new_achievement)
        db.session.commit()
        return jsonify(new_achievement.to_dict()), 201
    except Exception as e:
        db.session.rollback()
        print(f"Error creating achievement: {e}")
        return jsonify({"error": "An unexpected error occurred while creating the achievement."}), 500

@anchor_bp.route('/achievements', methods=['GET'])
@jwt_required()
def get_all_achievements():
    current_user_id_str = get_jwt_identity()
    try: current_user_id = int(current_user_id_str)
    except ValueError: return jsonify({"error": "Invalid user identity in token"}), 400
    user_achievements = Achievement.query.filter_by(user_id=current_user_id)\
        .order_by(Achievement.date_achieved.desc().nullslast(), Achievement.created_at.desc())\
        .all()
    return jsonify([ach.to_dict() for ach in user_achievements]), 200

@anchor_bp.route('/achievements/<int:achievement_id>', methods=['GET'])
@jwt_required()
def get_achievement_by_id(achievement_id):
    current_user_id_str = get_jwt_identity()
    try: current_user_id = int(current_user_id_str)
    except ValueError: return jsonify({"error": "Invalid user identity in token"}), 400
    achievement = db.session.get(Achievement, achievement_id)
    if not achievement: return jsonify({"error": "Achievement not found"}), 404
    if achievement.user_id != current_user_id: return jsonify({"error": "Forbidden: You do not have permission to access this achievement"}), 403
    return jsonify(achievement.to_dict()), 200

@anchor_bp.route('/achievements/<int:achievement_id>', methods=['PUT'])
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
        else: # Allow setting to null, which model's to_dict handles as []
             achievement.core_skills_json = None # Or [] if you prefer to always store a list
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
        return jsonify({"error": "An unexpected error occurred while updating the achievement."}), 500

@anchor_bp.route('/achievements/<int:achievement_id>', methods=['DELETE'])
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
        return jsonify({"error": "Error deleting achievement."}), 500

# --- Current Focus Section ("正在做什么") ---
# This section has been removed as Current Focus is now part of To-Do items.

# --- Future Plans Section ("打算做什么") ---
# (Future Plans CRUD endpoints remain unchanged)
@anchor_bp.route('/future_plans', methods=['POST'])
@jwt_required()
def create_future_plan():
    current_user_id_str = get_jwt_identity()
    try: current_user_id = int(current_user_id_str)
    except ValueError: return jsonify({"error": "Invalid user identity in token"}), 400
    data = request.get_json()
    if not data: return jsonify({"error": "Request body must be JSON"}), 400
    description = data.get('description')
    if not description or not isinstance(description, str) or not description.strip(): return jsonify({"error": "Description is required"}), 400
    new_plan = FuturePlan(user_id=current_user_id, description=description.strip())
    if 'goal_type' in data:
        goal_type = data.get('goal_type')
        if goal_type is not None and (not isinstance(goal_type, str) or len(goal_type) > 50): return jsonify({"error":"goal_type must be string max 50 chars or null"}),400
        new_plan.goal_type = goal_type.strip() if goal_type else None
    if 'status' in data:
        status = data.get('status').lower()
        if status not in ALLOWED_FUTURE_PLAN_STATUSES: return jsonify({"error": "Invalid status"}), 400
        new_plan.status = status
    else: new_plan.status = 'active' # Default
    if 'target_date' in data:
        date_str = data.get('target_date')
        if date_str is None: new_plan.target_date = None
        else:
            try: new_plan.target_date = datetime.datetime.strptime(date_str, '%Y-%m-%d').date()
            except ValueError: return jsonify({"error": "Invalid target_date format"}), 400
    try:
        db.session.add(new_plan)
        db.session.commit()
        return jsonify(new_plan.to_dict()), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": "Error creating future plan."}), 500

@anchor_bp.route('/future_plans', methods=['GET'])
@jwt_required()
def get_all_future_plans():
    current_user_id_str = get_jwt_identity()
    try: current_user_id = int(current_user_id_str)
    except ValueError: return jsonify({"error": "Invalid user identity in token"}), 400
    user_plans = FuturePlan.query.filter_by(user_id=current_user_id).order_by(FuturePlan.target_date.asc().nullslast(), FuturePlan.created_at.desc()).all()
    return jsonify([plan.to_dict() for plan in user_plans]), 200

@anchor_bp.route('/future_plans/<int:plan_id>', methods=['GET'])
@jwt_required()
def get_future_plan_by_id(plan_id):
    current_user_id_str = get_jwt_identity()
    try: current_user_id = int(current_user_id_str)
    except ValueError: return jsonify({"error": "Invalid user identity in token"}), 400
    plan = db.session.get(FuturePlan, plan_id)
    if not plan: return jsonify({"error": "Future plan not found"}), 404
    if plan.user_id != current_user_id: return jsonify({"error": "Forbidden"}), 403
    return jsonify(plan.to_dict()), 200

@anchor_bp.route('/future_plans/<int:plan_id>', methods=['PUT'])
@jwt_required()
def update_future_plan(plan_id):
    current_user_id_str = get_jwt_identity()
    try: current_user_id = int(current_user_id_str)
    except ValueError: return jsonify({"error": "Invalid user identity in token"}), 400
    plan = db.session.get(FuturePlan, plan_id)
    if not plan: return jsonify({"error": "Future plan not found"}), 404
    if plan.user_id != current_user_id: return jsonify({"error": "Forbidden"}), 403
    data = request.get_json()
    if not data: return jsonify({"error": "Request body must be JSON"}), 400
    updated_fields_count = 0
    if 'description' in data:
        desc = data.get('description')
        if not desc or not isinstance(desc, str) or not desc.strip(): return jsonify({"error":"Description must be non-empty string"}), 400
        plan.description = desc.strip(); updated_fields_count += 1
    if 'goal_type' in data:
        goal_type = data.get('goal_type')
        if goal_type is not None and (not isinstance(goal_type, str) or len(goal_type) > 50): return jsonify({"error":"goal_type must be string max 50 chars or null"}),400
        plan.goal_type = goal_type.strip() if goal_type else None; updated_fields_count += 1
    if 'status' in data:
        status = data.get('status').lower()
        if status not in ALLOWED_FUTURE_PLAN_STATUSES: return jsonify({"error":"Invalid status"}), 400
        plan.status = status; updated_fields_count += 1
    if 'target_date' in data:
        date_str = data.get('target_date')
        if date_str is None: plan.target_date = None
        else:
            try: plan.target_date = datetime.datetime.strptime(date_str, '%Y-%m-%d').date()
            except ValueError: return jsonify({"error":"Invalid target_date format"}), 400
        updated_fields_count += 1
    if updated_fields_count == 0 and data: return jsonify({"message":"No relevant fields to update"}), 200
    try:
        db.session.commit()
        return jsonify(plan.to_dict()), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": "Error updating future plan."}), 500

@anchor_bp.route('/future_plans/<int:plan_id>', methods=['DELETE'])
@jwt_required()
def delete_future_plan(plan_id):
    current_user_id_str = get_jwt_identity()
    try: current_user_id = int(current_user_id_str)
    except ValueError: return jsonify({"error": "Invalid user identity in token"}), 400
    plan = db.session.get(FuturePlan, plan_id)
    if not plan: return jsonify({"error": "Future plan not found"}), 404
    if plan.user_id != current_user_id: return jsonify({"error": "Forbidden"}), 403
    try:
        db.session.delete(plan)
        db.session.commit()
        return '', 204
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": "Error deleting future plan."}), 500
