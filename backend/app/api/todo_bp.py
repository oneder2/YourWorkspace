# /your_project_root/app/api/todo_bp.py
# Blueprint for To-Do list related API endpoints.

from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required, get_jwt_identity
import datetime # For handling date conversions if needed

# Import the TodoItem model and the db instance
from ..models.todo_item import TodoItem
from ..extensions import db

# Create a Blueprint instance named 'todo'
todo_bp = Blueprint('todo', __name__)

# Allowed values for status and priority - for validation
ALLOWED_STATUSES = ['pending', 'in_progress', 'completed', 'deferred']
ALLOWED_PRIORITIES = ['low', 'medium', 'high']

@todo_bp.route('/ping', methods=['GET'])
def ping_todo():
    """Simple test route to check if the todo blueprint is registered."""
    return jsonify({"message": "Todo API is alive!"}), 200

@todo_bp.route('/todos', methods=['GET'])
@jwt_required()
def get_all_todos():
    """
    Retrieves all to-do items for the currently authenticated user.
    """
    current_user_id_str = get_jwt_identity()
    try:
        current_user_id = int(current_user_id_str)
    except ValueError:
        return jsonify({"error": "Invalid user identity in token"}), 400

    user_todos = TodoItem.query.filter_by(user_id=current_user_id).order_by(TodoItem.created_at.desc()).all()
    todos_list = [todo.to_dict() for todo in user_todos]
    return jsonify(todos_list), 200

@todo_bp.route('/todos', methods=['POST'])
@jwt_required()
def create_todo():
    """
    Creates a new to-do item for the currently authenticated user.
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
        
    due_date_str = data.get('due_date')
    due_date_obj = None
    if due_date_str:
        try:
            due_date_obj = datetime.datetime.strptime(due_date_str, '%Y-%m-%d').date()
        except ValueError:
            return jsonify({"error": "Invalid due_date format. Please use YYYY-MM-DD."}), 400

    status = data.get('status', 'pending').lower()
    if status not in ALLOWED_STATUSES:
        return jsonify({"error": f"Invalid status. Allowed values are: {', '.join(ALLOWED_STATUSES)}"}), 400

    priority = data.get('priority', 'medium').lower()
    if priority not in ALLOWED_PRIORITIES:
        return jsonify({"error": f"Invalid priority. Allowed values are: {', '.join(ALLOWED_PRIORITIES)}"}), 400

    try:
        new_todo = TodoItem(
            user_id=current_user_id,
            title=title.strip(),
            description=description.strip() if description else None,
            due_date=due_date_obj,
            status=status,
            priority=priority
        )
        db.session.add(new_todo)
        db.session.commit()
        return jsonify(new_todo.to_dict()), 201
    except Exception as e:
        db.session.rollback()
        print(f"Error creating todo item: {e}")
        return jsonify({"error": "An unexpected error occurred while creating the to-do item."}), 500

@todo_bp.route('/todos/<int:todo_id>', methods=['GET'])
@jwt_required()
def get_todo_by_id(todo_id):
    """
    Retrieves a specific to-do item by its ID for the currently authenticated user.
    """
    current_user_id_str = get_jwt_identity()
    try:
        current_user_id = int(current_user_id_str)
    except ValueError:
        return jsonify({"error": "Invalid user identity in token"}), 400

    # Query for the specific to-do item by its ID and ensuring it belongs to the current user
    todo_item = db.session.get(TodoItem, todo_id) # Using db.session.get for SQLAlchemy 2.0+

    if not todo_item:
        return jsonify({"error": "To-do item not found"}), 404
    
    if todo_item.user_id != current_user_id:
        # User is trying to access a to-do item that doesn't belong to them
        return jsonify({"error": "Forbidden: You do not have permission to access this item"}), 403

    return jsonify(todo_item.to_dict()), 200


@todo_bp.route('/todos/<int:todo_id>', methods=['PUT'])
@jwt_required()
def update_todo(todo_id):
    """
    Updates an existing to-do item for the currently authenticated user.
    """
    current_user_id_str = get_jwt_identity()
    try:
        current_user_id = int(current_user_id_str)
    except ValueError:
        return jsonify({"error": "Invalid user identity in token"}), 400

    # Fetch the existing to-do item
    todo_item = db.session.get(TodoItem, todo_id) # Using db.session.get for SQLAlchemy 2.0+

    if not todo_item:
        return jsonify({"error": "To-do item not found"}), 404

    # Check if the to-do item belongs to the current user
    if todo_item.user_id != current_user_id:
        return jsonify({"error": "Forbidden: You do not have permission to update this item"}), 403

    data = request.get_json()
    if not data:
        return jsonify({"error": "Request body must be JSON and cannot be empty"}), 400

    # Update fields if they are provided in the request body
    if 'title' in data:
        title = data['title']
        if not title or not isinstance(title, str) or not title.strip():
            return jsonify({"error": "Title must be a non-empty string if provided"}), 400
        todo_item.title = title.strip()

    if 'description' in data:
        description = data['description']
        if description is not None and not isinstance(description, str):
             return jsonify({"error": "Description must be a string if provided"}), 400
        todo_item.description = description.strip() if description else None


    if 'due_date' in data:
        due_date_str = data['due_date']
        if due_date_str is None: # Allow setting due_date to null
            todo_item.due_date = None
        elif isinstance(due_date_str, str):
            try:
                todo_item.due_date = datetime.datetime.strptime(due_date_str, '%Y-%m-%d').date()
            except ValueError:
                return jsonify({"error": "Invalid due_date format. Please use YYYY-MM-DD or null."}), 400
        else:
            return jsonify({"error": "due_date must be a string in YYYY-MM-DD format or null."}), 400


    if 'status' in data:
        status = data['status'].lower()
        if status not in ALLOWED_STATUSES:
            return jsonify({"error": f"Invalid status. Allowed values are: {', '.join(ALLOWED_STATUSES)}"}), 400
        todo_item.status = status
        # If status is 'completed', set completed_at timestamp
        if status == 'completed' and todo_item.completed_at is None:
            todo_item.completed_at = datetime.datetime.now(datetime.timezone.utc)
        elif status != 'completed': # If status changes from completed, clear completed_at
            todo_item.completed_at = None


    if 'priority' in data:
        priority = data['priority'].lower()
        if priority not in ALLOWED_PRIORITIES:
            return jsonify({"error": f"Invalid priority. Allowed values are: {', '.join(ALLOWED_PRIORITIES)}"}), 400
        todo_item.priority = priority
    
    # The updated_at field will be automatically updated by the model's onupdate

    try:
        db.session.commit()
        return jsonify(todo_item.to_dict()), 200
    except Exception as e:
        db.session.rollback()
        print(f"Error updating todo item: {e}")
        return jsonify({"error": "An unexpected error occurred while updating the to-do item."}), 500


@todo_bp.route('/todos/<int:todo_id>', methods=['DELETE'])
@jwt_required()
def delete_todo(todo_id):
    """
    Deletes a specific to-do item for the currently authenticated user.
    """
    current_user_id_str = get_jwt_identity()
    try:
        current_user_id = int(current_user_id_str)
    except ValueError:
        return jsonify({"error": "Invalid user identity in token"}), 400

    # Fetch the to-do item
    todo_item = db.session.get(TodoItem, todo_id) # Using db.session.get for SQLAlchemy 2.0+

    if not todo_item:
        return jsonify({"error": "To-do item not found"}), 404

    # Check if the to-do item belongs to the current user
    if todo_item.user_id != current_user_id:
        return jsonify({"error": "Forbidden: You do not have permission to delete this item"}), 403

    try:
        db.session.delete(todo_item)
        db.session.commit()
        # Return a 204 No Content response, which is standard for successful DELETE operations
        # Alternatively, you can return a success message:
        # return jsonify({"message": "To-do item deleted successfully"}), 200
        return '', 204
    except Exception as e:
        db.session.rollback()
        print(f"Error deleting todo item: {e}")
        return jsonify({"error": "An unexpected error occurred while deleting the to-do item."}), 500
