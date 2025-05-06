# /your_project_root/app/api/todo_bp.py
# Blueprint for todo list related API endpoints (user-specific CRUD).

from flask import Blueprint, jsonify, request
# Import necessary components later (e.g., Todo model, schemas, db session, JWT decorator)
# from ...models.todo import Todo
# from ...schemas.todo_schema import TodoSchema
# from ...extensions import db
# from flask_jwt_extended import jwt_required, get_jwt_identity

# Create a Blueprint instance named 'todo'
todo_bp = Blueprint('todo', __name__)

# --- Placeholder Data (Remove when using database) ---
# Structure: { user_id: { task_id: { ...task_data... } } }
_todos = {
    1: { # User 1's todos
        101: {"id": 101, "text": "Learn Flask Blueprints", "completed": True, "user_id": 1},
        102: {"id": 102, "text": "Learn Svelte", "completed": False, "user_id": 1},
    },
    2: { # User 2's todos
        201: {"id": 201, "text": "Buy groceries", "completed": False, "user_id": 2},
    }
}
_next_todo_id = 301 # Global counter for simplicity, real app needs better ID generation

# --- Todo List Routes ---

@todo_bp.route('/ping', methods=['GET'])
def ping_todo():
    """Simple test route."""
    return jsonify({"message": "Todo API is alive!"}), 200


@todo_bp.route('/tasks', methods=['GET'])
#@jwt_required() # Protect this route
def get_tasks():
    """
    Endpoint to retrieve all todo tasks for the currently logged-in user.
    """
    # --- Add logic to fetch tasks for the current user from database ---
    # Example:
    # current_user_id = get_jwt_identity()
    # user_tasks = Todo.query.filter_by(user_id=current_user_id).order_by(Todo.created_at).all()
    # todo_schema = TodoSchema(many=True)
    # return jsonify(todo_schema.dump(user_tasks)), 200

    # Placeholder response:
    # current_user_id = get_jwt_identity() # Would fail without @jwt_required
    current_user_id = 1 # Placeholder user ID
    user_tasks_dict = _todos.get(current_user_id, {})
    return jsonify(list(user_tasks_dict.values())), 200


@todo_bp.route('/tasks/<int:task_id>', methods=['GET'])
#@jwt_required()
def get_task(task_id):
    """
    Endpoint to retrieve a single todo task by its ID.
    Ensures the task belongs to the currently logged-in user.
    """
    # --- Add logic to fetch a single task ensuring ownership ---
    # Example:
    # current_user_id = get_jwt_identity()
    # task = Todo.query.filter_by(id=task_id, user_id=current_user_id).first_or_404()
    # todo_schema = TodoSchema()
    # return jsonify(todo_schema.dump(task)), 200

    # Placeholder response:
    # current_user_id = get_jwt_identity() # Would fail without @jwt_required
    current_user_id = 1 # Placeholder user ID
    user_tasks_dict = _todos.get(current_user_id, {})
    task = user_tasks_dict.get(task_id)

    if task:
        return jsonify(task), 200
    else:
        # Return 404 even if task exists but belongs to another user for security
        return jsonify({"error": "Task not found"}), 404


@todo_bp.route('/tasks', methods=['POST'])
#@jwt_required()
def create_task():
    """
    Endpoint to create a new todo task for the currently logged-in user.
    Expects JSON data: {'text': '...'}
    """
    data = request.get_json()
    if not data or not data.get('text'):
        return jsonify({"error": "Missing required field (text)"}), 400

    # --- Add logic to create a task in the database ---
    # Example:
    # current_user_id = get_jwt_identity()
    # new_task = Todo(text=data['text'], user_id=current_user_id)
    # db.session.add(new_task)
    # db.session.commit()
    # todo_schema = TodoSchema()
    # return jsonify(todo_schema.dump(new_task)), 201

    # Placeholder response:
    global _next_todo_id
    # current_user_id = get_jwt_identity() # Would fail without @jwt_required
    current_user_id = 1 # Placeholder user ID

    new_task_data = {
        "id": _next_todo_id,
        "text": data['text'],
        "completed": False,
        "user_id": current_user_id
    }

    if current_user_id not in _todos:
        _todos[current_user_id] = {}
    _todos[current_user_id][_next_todo_id] = new_task_data
    _next_todo_id += 1

    return jsonify(new_task_data), 201


@todo_bp.route('/tasks/<int:task_id>', methods=['PUT'])
#@jwt_required()
def update_task(task_id):
    """
    Endpoint to update an existing todo task (e.g., mark as completed, change text).
    Expects JSON data: {'text': '...', 'completed': ...} (at least one)
    Ensures the task belongs to the currently logged-in user.
    """
    data = request.get_json()
    if not data or ('text' not in data and 'completed' not in data):
        return jsonify({"error": "Missing fields to update (text or completed)"}), 400

    # --- Add logic to update a task in the database ---
    # Example:
    # current_user_id = get_jwt_identity()
    # task = Todo.query.filter_by(id=task_id, user_id=current_user_id).first_or_404()
    #
    # if 'text' in data:
    #     task.text = data['text']
    # if 'completed' in data:
    #     task.completed = data['completed']
    #
    # db.session.commit()
    # todo_schema = TodoSchema()
    # return jsonify(todo_schema.dump(task)), 200

    # Placeholder response:
    # current_user_id = get_jwt_identity() # Would fail without @jwt_required
    current_user_id = 1 # Placeholder user ID
    user_tasks_dict = _todos.get(current_user_id, {})
    task = user_tasks_dict.get(task_id)

    if not task:
        return jsonify({"error": "Task not found"}), 404

    if 'text' in data:
        task['text'] = data['text']
    if 'completed' in data:
        task['completed'] = data['completed']

    return jsonify(task), 200


@todo_bp.route('/tasks/<int:task_id>', methods=['DELETE'])
#@jwt_required()
def delete_task(task_id):
    """
    Endpoint to delete a todo task.
    Ensures the task belongs to the currently logged-in user.
    """
    # --- Add logic to delete a task from the database ---
    # Example:
    # current_user_id = get_jwt_identity()
    # task = Todo.query.filter_by(id=task_id, user_id=current_user_id).first_or_404()
    #
    # db.session.delete(task)
    # db.session.commit()
    # return '', 204 # No Content response

    # Placeholder response:
    # current_user_id = get_jwt_identity() # Would fail without @jwt_required
    current_user_id = 1 # Placeholder user ID
    user_tasks_dict = _todos.get(current_user_id, {})

    if task_id in user_tasks_dict:
        del user_tasks_dict[task_id]
        # If the user has no more tasks, remove the user entry (optional)
        # if not user_tasks_dict:
        #     del _todos[current_user_id]
        return '', 204 # No Content
    else:
        return jsonify({"error": "Task not found"}), 404
