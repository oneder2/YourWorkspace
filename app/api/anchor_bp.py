# /your_project_root/app/api/anchor_bp.py
# Blueprint for "Personal Anchor Overview" related API endpoints.

from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required, get_jwt_identity
import datetime

# Import models
from ..models.user import User
from ..models.user_profile import UserProfile
from ..models.achievement import Achievement
from ..models.current_focus_item import CurrentFocusItem
from ..models.future_plan import FuturePlan # Import FuturePlan model
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
# (GET /profile and PUT /profile endpoints remain unchanged)
@anchor_bp.route('/profile', methods=['GET'])
@jwt_required()
def get_user_anchor_profile():
    """
    Retrieves the professional profile (title, bio) for the currently authenticated user.
    If a profile doesn't exist for an existing user, it creates an empty profile.
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
        try:
            new_profile = UserProfile(id=user.id)
            user.profile = new_profile
            db.session.add(new_profile)
            db.session.commit()
            print(f"INFO: Created missing profile for user_id: {user.id}")
        except Exception as e:
            db.session.rollback()
            print(f"ERROR: Could not create missing profile for user_id {user.id}: {e}")
            return jsonify({"error": "Could not retrieve or create user profile."}), 500
        
        if not user.profile:
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

    if not user.profile:
        print(f"INFO: Profile missing for user_id {user.id} during PUT, creating now.")
        try:
            user.profile = UserProfile(id=user.id)
            db.session.add(user.profile)
        except Exception as e:
            db.session.rollback()
            print(f"ERROR: Could not create missing profile during PUT for user_id {user.id}: {e}")
            return jsonify({"error": "Could not initialize user profile for update."}), 500

    data = request.get_json()
    if not data:
        return jsonify({"error": "Request body must be JSON and cannot be empty"}), 400

    updated = False

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
        db.session.commit()
        return jsonify(user.profile.to_dict()), 200
    except Exception as e:
        db.session.rollback()
        print(f"Error updating user profile: {e}")
        return jsonify({"error": "An unexpected error occurred while updating the profile."}), 500

# --- Achievements Section ("做过什么") ---
# (POST /achievements, GET /achievements, GET /achievements/<id>, PUT /achievements/<id>, DELETE /achievements/<id> remain unchanged)
@anchor_bp.route('/achievements', methods=['POST'])
@jwt_required()
def create_achievement():
    """
    Creates a new achievement for the currently authenticated user.
    """
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

    core_skills_json = data.get('core_skills_json')
    if core_skills_json is not None:
        if not isinstance(core_skills_json, list):
            return jsonify({"error": "core_skills_json must be a list of strings if provided"}), 400
        if not all(isinstance(skill, str) for skill in core_skills_json):
            return jsonify({"error": "All items in core_skills_json must be strings"}), 400
    
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
            core_skills_json=core_skills_json if core_skills_json else [],
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
    """
    Retrieves all achievements for the currently authenticated user.
    """
    current_user_id_str = get_jwt_identity()
    try:
        current_user_id = int(current_user_id_str)
    except ValueError:
        return jsonify({"error": "Invalid user identity in token"}), 400

    user_achievements = Achievement.query.filter_by(user_id=current_user_id)\
        .order_by(Achievement.date_achieved.desc().nullslast(), Achievement.created_at.desc())\
        .all()

    achievements_list = [ach.to_dict() for ach in user_achievements]
    return jsonify(achievements_list), 200

@anchor_bp.route('/achievements/<int:achievement_id>', methods=['GET'])
@jwt_required()
def get_achievement_by_id(achievement_id):
    """
    Retrieves a specific achievement by its ID for the currently authenticated user.
    """
    current_user_id_str = get_jwt_identity()
    try:
        current_user_id = int(current_user_id_str)
    except ValueError:
        return jsonify({"error": "Invalid user identity in token"}), 400

    achievement = db.session.get(Achievement, achievement_id)

    if not achievement:
        return jsonify({"error": "Achievement not found"}), 404

    if achievement.user_id != current_user_id:
        return jsonify({"error": "Forbidden: You do not have permission to access this achievement"}), 403

    return jsonify(achievement.to_dict()), 200


@anchor_bp.route('/achievements/<int:achievement_id>', methods=['PUT'])
@jwt_required()
def update_achievement(achievement_id):
    """
    Updates an existing achievement for the currently authenticated user.
    """
    current_user_id_str = get_jwt_identity()
    try:
        current_user_id = int(current_user_id_str)
    except ValueError:
        return jsonify({"error": "Invalid user identity in token"}), 400

    achievement = db.session.get(Achievement, achievement_id)

    if not achievement:
        return jsonify({"error": "Achievement not found"}), 404

    if achievement.user_id != current_user_id:
        return jsonify({"error": "Forbidden: You do not have permission to update this achievement"}), 403

    data = request.get_json()
    if not data:
        return jsonify({"error": "Request body must be JSON and cannot be empty"}), 400

    updated = False

    if 'title' in data:
        title = data['title']
        if not title or not isinstance(title, str) or not title.strip():
            return jsonify({"error": "Title is required and must be a non-empty string"}), 400
        achievement.title = title.strip()
        updated = True

    if 'description' in data:
        description = data['description']
        if description is not None and not isinstance(description, str):
            return jsonify({"error": "Description must be a string if provided"}), 400
        achievement.description = description.strip() if description else None
        updated = True

    if 'quantifiable_results' in data:
        quantifiable_results = data['quantifiable_results']
        if quantifiable_results is not None and not isinstance(quantifiable_results, str):
            return jsonify({"error": "Quantifiable results must be a string if provided"}), 400
        achievement.quantifiable_results = quantifiable_results.strip() if quantifiable_results else None
        updated = True

    if 'core_skills_json' in data:
        core_skills_json = data['core_skills_json']
        if core_skills_json is not None:
            if not isinstance(core_skills_json, list):
                return jsonify({"error": "core_skills_json must be a list of strings if provided"}), 400
            if not all(isinstance(skill, str) for skill in core_skills_json):
                return jsonify({"error": "All items in core_skills_json must be strings"}), 400
            achievement.core_skills_json = core_skills_json
        else:
             achievement.core_skills_json = []
        updated = True

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
        updated = True

    if not updated and data:
        return jsonify({"message": "No relevant achievement fields provided for update."}), 200

    try:
        db.session.commit()
        return jsonify(achievement.to_dict()), 200
    except Exception as e:
        db.session.rollback()
        print(f"Error updating achievement: {e}")
        return jsonify({"error": "An unexpected error occurred while updating the achievement."}), 500


@anchor_bp.route('/achievements/<int:achievement_id>', methods=['DELETE'])
@jwt_required()
def delete_achievement(achievement_id):
    """
    Deletes a specific achievement for the currently authenticated user.
    """
    current_user_id_str = get_jwt_identity()
    try:
        current_user_id = int(current_user_id_str)
    except ValueError:
        return jsonify({"error": "Invalid user identity in token"}), 400

    achievement = db.session.get(Achievement, achievement_id)

    if not achievement:
        return jsonify({"error": "Achievement not found"}), 404

    if achievement.user_id != current_user_id:
        return jsonify({"error": "Forbidden: You do not have permission to delete this achievement"}), 403

    try:
        db.session.delete(achievement)
        db.session.commit()
        return '', 204
    except Exception as e:
        db.session.rollback()
        print(f"Error deleting achievement: {e}")
        return jsonify({"error": "An unexpected error occurred while deleting the achievement."}), 500


# --- Current Focus Section ("正在做什么") ---
# (POST /current_focus, GET /current_focus, GET /current_focus/<id>, PUT /current_focus/<id>, DELETE /current_focus/<id> remain unchanged)
@anchor_bp.route('/current_focus', methods=['POST'])
@jwt_required()
def create_current_focus_item():
    """
    Creates a new current focus item for the currently authenticated user.
    """
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

    item_type = data.get('item_type')
    if item_type is not None and (not isinstance(item_type, str) or len(item_type) > 50):
         return jsonify({"error": "item_type must be a string with max 50 characters if provided"}), 400

    description = data.get('description')
    if description is not None and not isinstance(description, str):
        return jsonify({"error": "Description must be a string if provided"}), 400

    status = data.get('status')
    if status is not None and (not isinstance(status, str) or len(status) > 50):
         return jsonify({"error": "status must be a string with max 50 characters if provided"}), 400

    start_date_str = data.get('start_date')
    start_date_obj = None
    if start_date_str:
        try:
            start_date_obj = datetime.datetime.strptime(start_date_str, '%Y-%m-%d').date()
        except ValueError:
            return jsonify({"error": "Invalid start_date format. Please use YYYY-MM-DD."}), 400

    try:
        new_focus_item = CurrentFocusItem(
            user_id=current_user_id,
            title=title.strip(),
            item_type=item_type.strip() if item_type else None,
            description=description.strip() if description else None,
            start_date=start_date_obj,
            status=status.strip() if status else None
        )
        db.session.add(new_focus_item)
        db.session.commit()
        return jsonify(new_focus_item.to_dict()), 201
    except Exception as e:
        db.session.rollback()
        print(f"Error creating current focus item: {e}")
        return jsonify({"error": "An unexpected error occurred while creating the current focus item."}), 500


@anchor_bp.route('/current_focus', methods=['GET'])
@jwt_required()
def get_all_current_focus_items():
    """
    Retrieves all current focus items for the currently authenticated user.
    """
    current_user_id_str = get_jwt_identity()
    try:
        current_user_id = int(current_user_id_str)
    except ValueError:
        return jsonify({"error": "Invalid user identity in token"}), 400

    user_focus_items = CurrentFocusItem.query.filter_by(user_id=current_user_id)\
        .order_by(CurrentFocusItem.created_at.desc())\
        .all()

    focus_items_list = [item.to_dict() for item in user_focus_items]
    return jsonify(focus_items_list), 200

@anchor_bp.route('/current_focus/<int:focus_id>', methods=['GET'])
@jwt_required()
def get_current_focus_item_by_id(focus_id):
    """
    Retrieves a specific current focus item by its ID for the currently authenticated user.
    """
    current_user_id_str = get_jwt_identity()
    try:
        current_user_id = int(current_user_id_str)
    except ValueError:
        return jsonify({"error": "Invalid user identity in token"}), 400

    focus_item = db.session.get(CurrentFocusItem, focus_id)

    if not focus_item:
        return jsonify({"error": "Current focus item not found"}), 404

    if focus_item.user_id != current_user_id:
        return jsonify({"error": "Forbidden: You do not have permission to access this item"}), 403

    return jsonify(focus_item.to_dict()), 200


@anchor_bp.route('/current_focus/<int:focus_id>', methods=['PUT'])
@jwt_required()
def update_current_focus_item(focus_id):
    """
    Updates an existing current focus item for the currently authenticated user.
    """
    current_user_id_str = get_jwt_identity()
    try:
        current_user_id = int(current_user_id_str)
    except ValueError:
        return jsonify({"error": "Invalid user identity in token"}), 400

    focus_item = db.session.get(CurrentFocusItem, focus_id)

    if not focus_item:
        return jsonify({"error": "Current focus item not found"}), 404

    if focus_item.user_id != current_user_id:
        return jsonify({"error": "Forbidden: You do not have permission to update this item"}), 403

    data = request.get_json()
    if not data:
        return jsonify({"error": "Request body must be JSON and cannot be empty"}), 400

    updated = False

    if 'title' in data:
        title = data['title']
        if not title or not isinstance(title, str) or not title.strip():
            return jsonify({"error": "Title is required and must be a non-empty string"}), 400
        focus_item.title = title.strip()
        updated = True

    if 'item_type' in data:
        item_type = data['item_type']
        if item_type is not None and (not isinstance(item_type, str) or len(item_type) > 50):
            return jsonify({"error": "item_type must be a string with max 50 characters or null"}), 400
        focus_item.item_type = item_type.strip() if item_type else None
        updated = True

    if 'description' in data:
        description = data['description']
        if description is not None and not isinstance(description, str):
            return jsonify({"error": "Description must be a string or null"}), 400
        focus_item.description = description.strip() if description else None
        updated = True

    if 'status' in data:
        status = data['status']
        if status is not None and (not isinstance(status, str) or len(status) > 50):
            return jsonify({"error": "status must be a string with max 50 characters or null"}), 400
        focus_item.status = status.strip() if status else None
        updated = True

    if 'start_date' in data:
        start_date_str = data['start_date']
        if start_date_str is None:
             focus_item.start_date = None
        elif isinstance(start_date_str, str):
            try:
                focus_item.start_date = datetime.datetime.strptime(start_date_str, '%Y-%m-%d').date()
            except ValueError:
                return jsonify({"error": "Invalid start_date format. Please use YYYY-MM-DD or null."}), 400
        else:
             return jsonify({"error": "start_date must be a string in YYYY-MM-DD format or null."}), 400
        updated = True

    if not updated and data:
        return jsonify({"message": "No relevant current focus fields provided for update."}), 200

    try:
        db.session.commit()
        return jsonify(focus_item.to_dict()), 200
    except Exception as e:
        db.session.rollback()
        print(f"Error updating current focus item: {e}")
        return jsonify({"error": "An unexpected error occurred while updating the current focus item."}), 500


@anchor_bp.route('/current_focus/<int:focus_id>', methods=['DELETE'])
@jwt_required()
def delete_current_focus_item(focus_id):
    """
    Deletes a specific current focus item for the currently authenticated user.
    """
    current_user_id_str = get_jwt_identity()
    try:
        current_user_id = int(current_user_id_str)
    except ValueError:
        return jsonify({"error": "Invalid user identity in token"}), 400

    focus_item = db.session.get(CurrentFocusItem, focus_id)

    if not focus_item:
        return jsonify({"error": "Current focus item not found"}), 404

    if focus_item.user_id != current_user_id:
        return jsonify({"error": "Forbidden: You do not have permission to delete this item"}), 403

    try:
        db.session.delete(focus_item)
        db.session.commit()
        return '', 204
    except Exception as e:
        db.session.rollback()
        print(f"Error deleting current focus item: {e}")
        return jsonify({"error": "An unexpected error occurred while deleting the current focus item."}), 500

# --- Future Plans Section ("打算做什么") ---

@anchor_bp.route('/future_plans', methods=['POST'])
@jwt_required()
def create_future_plan():
    """
    Creates a new future plan for the currently authenticated user.
    """
    current_user_id_str = get_jwt_identity()
    try:
        current_user_id = int(current_user_id_str)
    except ValueError:
        return jsonify({"error": "Invalid user identity in token"}), 400

    data = request.get_json()
    if not data:
        return jsonify({"error": "Request body must be JSON"}), 400

    description = data.get('description')
    if not description or not isinstance(description, str) or not description.strip():
        return jsonify({"error": "Description is required and must be a non-empty string"}), 400

    goal_type = data.get('goal_type')
    if goal_type is not None and (not isinstance(goal_type, str) or len(goal_type) > 50):
         return jsonify({"error": "goal_type must be a string with max 50 characters if provided"}), 400

    status = data.get('status', 'active').lower()
    if status not in ALLOWED_FUTURE_PLAN_STATUSES:
        return jsonify({"error": f"Invalid status. Allowed values are: {', '.join(ALLOWED_FUTURE_PLAN_STATUSES)}"}), 400

    target_date_str = data.get('target_date')
    target_date_obj = None
    if target_date_str:
        try:
            target_date_obj = datetime.datetime.strptime(target_date_str, '%Y-%m-%d').date()
        except ValueError:
            return jsonify({"error": "Invalid target_date format. Please use YYYY-MM-DD."}), 400

    try:
        new_plan = FuturePlan(
            user_id=current_user_id,
            description=description.strip(),
            goal_type=goal_type.strip() if goal_type else None,
            target_date=target_date_obj,
            status=status
        )
        db.session.add(new_plan)
        db.session.commit()
        return jsonify(new_plan.to_dict()), 201
    except Exception as e:
        db.session.rollback()
        print(f"Error creating future plan: {e}")
        return jsonify({"error": "An unexpected error occurred while creating the future plan."}), 500


@anchor_bp.route('/future_plans', methods=['GET'])
@jwt_required()
def get_all_future_plans():
    """
    Retrieves all future plans for the currently authenticated user.
    """
    current_user_id_str = get_jwt_identity()
    try:
        current_user_id = int(current_user_id_str)
    except ValueError:
        return jsonify({"error": "Invalid user identity in token"}), 400

    user_plans = FuturePlan.query.filter_by(user_id=current_user_id)\
        .order_by(FuturePlan.target_date.asc().nullslast(), FuturePlan.created_at.desc())\
        .all()

    plans_list = [plan.to_dict() for plan in user_plans]
    return jsonify(plans_list), 200

@anchor_bp.route('/future_plans/<int:plan_id>', methods=['GET'])
@jwt_required()
def get_future_plan_by_id(plan_id):
    """
    Retrieves a specific future plan by its ID for the currently authenticated user.
    """
    current_user_id_str = get_jwt_identity()
    try:
        current_user_id = int(current_user_id_str)
    except ValueError:
        return jsonify({"error": "Invalid user identity in token"}), 400

    # Fetch the plan by its ID
    plan = db.session.get(FuturePlan, plan_id)

    if not plan:
        return jsonify({"error": "Future plan not found"}), 404

    # Verify ownership
    if plan.user_id != current_user_id:
        return jsonify({"error": "Forbidden: You do not have permission to access this plan"}), 403

    return jsonify(plan.to_dict()), 200


@anchor_bp.route('/future_plans/<int:plan_id>', methods=['PUT'])
@jwt_required()
def update_future_plan(plan_id):
    """
    Updates an existing future plan for the currently authenticated user.
    """
    current_user_id_str = get_jwt_identity()
    try:
        current_user_id = int(current_user_id_str)
    except ValueError:
        return jsonify({"error": "Invalid user identity in token"}), 400

    # Fetch the existing plan
    plan = db.session.get(FuturePlan, plan_id)

    if not plan:
        return jsonify({"error": "Future plan not found"}), 404

    # Verify ownership
    if plan.user_id != current_user_id:
        return jsonify({"error": "Forbidden: You do not have permission to update this plan"}), 403

    data = request.get_json()
    if not data:
        return jsonify({"error": "Request body must be JSON and cannot be empty"}), 400

    updated = False

    # Update fields based on request data, with validation
    if 'description' in data:
        description = data['description']
        if not description or not isinstance(description, str) or not description.strip():
             return jsonify({"error": "Description is required and must be a non-empty string"}), 400
        plan.description = description.strip()
        updated = True

    if 'goal_type' in data:
        goal_type = data['goal_type']
        if goal_type is not None and (not isinstance(goal_type, str) or len(goal_type) > 50):
            return jsonify({"error": "goal_type must be a string with max 50 characters or null"}), 400
        plan.goal_type = goal_type.strip() if goal_type else None
        updated = True

    if 'status' in data:
        status = data['status'].lower()
        if status not in ALLOWED_FUTURE_PLAN_STATUSES:
             return jsonify({"error": f"Invalid status. Allowed values are: {', '.join(ALLOWED_FUTURE_PLAN_STATUSES)}"}), 400
        plan.status = status
        updated = True

    if 'target_date' in data:
        target_date_str = data['target_date']
        if target_date_str is None:
             plan.target_date = None
        elif isinstance(target_date_str, str):
            try:
                plan.target_date = datetime.datetime.strptime(target_date_str, '%Y-%m-%d').date()
            except ValueError:
                return jsonify({"error": "Invalid target_date format. Please use YYYY-MM-DD or null."}), 400
        else:
             return jsonify({"error": "target_date must be a string in YYYY-MM-DD format or null."}), 400
        updated = True

    if not updated and data:
        return jsonify({"message": "No relevant future plan fields provided for update."}), 200

    try:
        db.session.commit()
        return jsonify(plan.to_dict()), 200
    except Exception as e:
        db.session.rollback()
        print(f"Error updating future plan: {e}")
        return jsonify({"error": "An unexpected error occurred while updating the future plan."}), 500


@anchor_bp.route('/future_plans/<int:plan_id>', methods=['DELETE'])
@jwt_required()
def delete_future_plan(plan_id):
    """
    Deletes a specific future plan for the currently authenticated user.
    """
    current_user_id_str = get_jwt_identity()
    try:
        current_user_id = int(current_user_id_str)
    except ValueError:
        return jsonify({"error": "Invalid user identity in token"}), 400

    # Fetch the plan
    plan = db.session.get(FuturePlan, plan_id)

    if not plan:
        return jsonify({"error": "Future plan not found"}), 404

    # Verify ownership
    if plan.user_id != current_user_id:
        return jsonify({"error": "Forbidden: You do not have permission to delete this plan"}), 403

    try:
        db.session.delete(plan)
        db.session.commit()
        return '', 204 # No Content
    except Exception as e:
        db.session.rollback()
        print(f"Error deleting future plan: {e}")
        return jsonify({"error": "An unexpected error occurred while deleting the future plan."}), 500

