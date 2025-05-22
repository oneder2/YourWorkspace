# /your_project_root/app/api/todo_bp.py
# Blueprint for To-Do list related API endpoints.

from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
import datetime # For handling date conversions if needed

# Import the TodoItem model and the db instance
from ..models.todo_item import TodoItem
from ..extensions import db

# Import standardized API response utilities
from ..utils.api_responses import api_success, api_error, api_validation_error
from ..utils.request_validation import validate_json_request, validate_field_type, validate_enum_field

# Create a Blueprint instance named 'todo'
todo_bp = Blueprint('todo', __name__)

# Allowed values for status and priority - for validation
ALLOWED_STATUSES = ['pending', 'in_progress', 'completed', 'deferred']
ALLOWED_PRIORITIES = ['low', 'medium', 'high']

@todo_bp.route('/ping', methods=['GET'])
# This is a simple test route for the blueprint, not JWT protected for basic check
def ping_todo():
    """Simple test route to check if the todo blueprint is registered."""
    return api_success(message="Todo API is alive!")

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
        return api_error("Invalid user identity in token", 400)

    # is_current_focus = True items will be listed first, then by created_at desc.
    user_todos = TodoItem.query.filter_by(user_id=current_user_id)\
        .order_by(TodoItem.is_current_focus.desc(), TodoItem.created_at.desc())\
        .all()
    todos_list = [todo.to_dict() for todo in user_todos]
    return api_success(data=todos_list)

@todo_bp.route('/todos', methods=['POST'])
@jwt_required() # Protect this route
@validate_json_request(required_fields=['title'])
def create_todo():
    """
    Creates a new to-do item for the currently authenticated user.
    The 'is_current_focus' field defaults to False in the model and is not typically set on creation.
    """
    current_user_id_str = get_jwt_identity()
    try:
        current_user_id = int(current_user_id_str)
    except ValueError:
        return api_error("Invalid user identity in token", 400)

    data = request.get_json()

    # Validate title
    title = data.get('title')
    if not title or not isinstance(title, str) or not title.strip():
        return api_validation_error({"title": ["Title is required and must be a non-empty string"]})

    # Validate description
    description = data.get('description')
    description_error = validate_field_type(data, 'description', str)
    if description_error:
        return api_validation_error({"description": [description_error]})

    # Validate due_date
    due_date_str = data.get('due_date')
    due_date_obj = None
    if due_date_str:
        try:
            due_date_obj = datetime.datetime.strptime(due_date_str, '%Y-%m-%d').date()
        except ValueError:
            return api_validation_error({"due_date": ["Invalid date format. Please use YYYY-MM-DD."]})

    # Validate status
    status = data.get('status', 'pending').lower()
    status_error = validate_enum_field(data, 'status', ALLOWED_STATUSES)
    if status_error:
        return api_validation_error({"status": [status_error]})

    # Validate priority
    priority = data.get('priority', 'medium').lower()
    priority_error = validate_enum_field(data, 'priority', ALLOWED_PRIORITIES)
    if priority_error:
        return api_validation_error({"priority": [priority_error]})

    # Validate is_current_focus if provided
    is_current_focus = data.get('is_current_focus')
    if is_current_focus is not None and not isinstance(is_current_focus, bool):
        return api_validation_error({"is_current_focus": ["Must be a boolean value"]})

    try:
        new_todo = TodoItem(
            user_id=current_user_id,
            title=title.strip(),
            description=description.strip() if description else None,
            due_date=due_date_obj,
            status=status,
            priority=priority,
            is_current_focus=is_current_focus if is_current_focus is not None else False
        )
        db.session.add(new_todo)
        db.session.commit()
        return api_success(data=new_todo.to_dict(), status_code=201,
                          message="Todo item created successfully")
    except Exception as e:
        db.session.rollback()
        print(f"Error creating todo item: {e}")
        return api_error("An unexpected error occurred while creating the to-do item.", 500)

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
        return api_error("Invalid user identity in token", 400)

    todo_item = db.session.get(TodoItem, todo_id)

    if not todo_item:
        return api_error("To-do item not found", 404)

    if todo_item.user_id != current_user_id:
        return api_error("Forbidden: You do not have permission to access this item", 403)

    return api_success(data=todo_item.to_dict())


@todo_bp.route('/todos/<int:todo_id>', methods=['PUT'])
@jwt_required()
def update_todo(todo_id):
    """
    Updates an existing to-do item for the currently authenticated user.
    Can update standard fields and the 'is_current_focus' flag.
    """
    current_user_id_str = get_jwt_identity()
    try:
        current_user_id = int(current_user_id_str)
    except ValueError:
        return jsonify({"error": "Invalid user identity in token"}), 400

    todo_item = db.session.get(TodoItem, todo_id)

    if not todo_item:
        return jsonify({"error": "To-do item not found"}), 404

    if todo_item.user_id != current_user_id:
        return jsonify({"error": "Forbidden: You do not have permission to update this item"}), 403

    data = request.get_json()
    if not data:
        return jsonify({"error": "Request body must be JSON and cannot be empty"}), 400

    updated_fields = False # Flag to track if any updatable field was actually sent

    if 'title' in data:
        title = data['title']
        if not title or not isinstance(title, str) or not title.strip():
            return jsonify({"error": "Title must be a non-empty string if provided"}), 400
        todo_item.title = title.strip()
        updated_fields = True

    if 'description' in data:
        description = data['description']
        if description is not None and not isinstance(description, str):
             return jsonify({"error": "Description must be a string if provided"}), 400
        todo_item.description = description.strip() if description else None
        updated_fields = True

    if 'due_date' in data:
        due_date_str = data['due_date']
        if due_date_str is None:
            todo_item.due_date = None
        elif isinstance(due_date_str, str):
            try:
                todo_item.due_date = datetime.datetime.strptime(due_date_str, '%Y-%m-%d').date()
            except ValueError:
                return jsonify({"error": "Invalid due_date format. Please use YYYY-MM-DD or null."}), 400
        else:
            return jsonify({"error": "due_date must be a string in YYYY-MM-DD format or null."}), 400
        updated_fields = True

    if 'status' in data:
        status = data['status'].lower()
        if status not in ALLOWED_STATUSES:
            return jsonify({"error": f"Invalid status. Allowed values are: {', '.join(ALLOWED_STATUSES)}"}), 400
        todo_item.status = status
        if status == 'completed' and todo_item.completed_at is None:
            todo_item.completed_at = datetime.datetime.now(datetime.timezone.utc)
        elif status != 'completed':
            todo_item.completed_at = None
        updated_fields = True

    if 'priority' in data:
        priority = data['priority'].lower()
        if priority not in ALLOWED_PRIORITIES:
            return jsonify({"error": f"Invalid priority. Allowed values are: {', '.join(ALLOWED_PRIORITIES)}"}), 400
        todo_item.priority = priority
        updated_fields = True

    # Handle 'is_current_focus' update
    if 'is_current_focus' in data:
        is_focus = data['is_current_focus']
        if not isinstance(is_focus, bool):
            return jsonify({"error": "is_current_focus must be a boolean"}), 400
        todo_item.is_current_focus = is_focus
        updated_fields = True

    if not updated_fields and data: # Data was sent, but no recognized fields for update
         return jsonify({"message": "No relevant to-do fields provided for update."}), 200

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

    todo_item = db.session.get(TodoItem, todo_id)

    if not todo_item:
        return jsonify({"error": "To-do item not found"}), 404

    if todo_item.user_id != current_user_id:
        return jsonify({"error": "Forbidden: You do not have permission to delete this item"}), 403

    try:
        db.session.delete(todo_item)
        db.session.commit()
        return '', 204
    except Exception as e:
        db.session.rollback()
        print(f"Error deleting todo item: {e}")
        return jsonify({"error": "An unexpected error occurred while deleting the to-do item."}), 500
