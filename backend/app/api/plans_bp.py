# /your_project_root/app/api/plans_bp.py
# Blueprint for "Future Plans" (Plan) related API endpoints.

from flask import Blueprint, jsonify, request, current_app
from flask_jwt_extended import jwt_required, get_jwt_identity
import datetime

# Import models and db instance
from ..models.user import User # Assuming User model might be needed for context
from ..models.future_plan import FuturePlan
from ..extensions import db

# Create a Blueprint instance named 'plans'
plans_bp = Blueprint('plans', __name__)

# Allowed values for FuturePlan status - for validation
ALLOWED_FUTURE_PLAN_STATUSES = ['active', 'achieved', 'deferred', 'abandoned']

@plans_bp.route('/ping', methods=['GET'])
def ping_plans():
    """Simple test route to check if the plans blueprint is registered."""
    return jsonify({"message": "Plans API is alive!"}), 200

# --- Future Plans Section ("打算做什么") ---
@plans_bp.route('/', methods=['POST']) # Changed from '/future_plans' to '/'
@jwt_required()
def create_future_plan():
    current_user_id_str = get_jwt_identity()
    try: current_user_id = int(current_user_id_str)
    except ValueError: return jsonify({"error": "Invalid user identity in token"}), 400
    data = request.get_json()
    if not data: return jsonify({"error": "Request body must be JSON"}), 400

    title = data.get('title')
    if not title or not isinstance(title, str) or not title.strip():
        return jsonify({"error": "Title is required"}), 400

    description = data.get('description')
    if not description or not isinstance(description, str) or not description.strip():
        return jsonify({"error": "Description is required"}), 400

    new_plan = FuturePlan(
        user_id=current_user_id,
        title=title.strip(),
        description=description.strip()
    )
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
        current_app.logger.error(f"Error creating future plan: {e}", exc_info=True)
        return jsonify({"error": "Error creating future plan."}), 500

@plans_bp.route('/', methods=['GET']) # Changed from '/future_plans' to '/'
@jwt_required()
def get_all_future_plans():
    current_user_id_str = get_jwt_identity()
    try: current_user_id = int(current_user_id_str)
    except ValueError: return jsonify({"error": "Invalid user identity in token"}), 400
    user_plans = FuturePlan.query.filter_by(user_id=current_user_id).order_by(FuturePlan.target_date.asc().nullslast(), FuturePlan.created_at.desc()).all()
    return jsonify([plan.to_dict() for plan in user_plans]), 200

@plans_bp.route('/<int:plan_id>', methods=['GET']) # Changed from '/future_plans/<id>' to '/<id>'
@jwt_required()
def get_future_plan_by_id(plan_id):
    current_user_id_str = get_jwt_identity()
    try: current_user_id = int(current_user_id_str)
    except ValueError: return jsonify({"error": "Invalid user identity in token"}), 400
    plan = db.session.get(FuturePlan, plan_id)
    if not plan: return jsonify({"error": "Future plan not found"}), 404
    if plan.user_id != current_user_id: return jsonify({"error": "Forbidden"}), 403
    return jsonify(plan.to_dict()), 200

@plans_bp.route('/<int:plan_id>', methods=['PUT']) # Changed from '/future_plans/<id>' to '/<id>'
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

    if 'title' in data:
        title = data.get('title')
        if not title or not isinstance(title, str) or not title.strip():
            return jsonify({"error":"Title must be non-empty string"}), 400
        plan.title = title.strip()
        updated_fields_count += 1

    if 'description' in data:
        desc = data.get('description')
        if not desc or not isinstance(desc, str) or not desc.strip():
            return jsonify({"error":"Description must be non-empty string"}), 400
        plan.description = desc.strip()
        updated_fields_count += 1
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
        current_app.logger.error(f"Error updating future plan: {e}", exc_info=True)
        return jsonify({"error": "Error updating future plan."}), 500

@plans_bp.route('/<int:plan_id>', methods=['DELETE']) # Changed from '/future_plans/<id>' to '/<id>'
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
        current_app.logger.error(f"Error deleting future plan: {e}", exc_info=True)
        return jsonify({"error": "Error deleting future plan."}), 500
