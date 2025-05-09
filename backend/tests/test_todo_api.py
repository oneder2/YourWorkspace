# /your_project_root/tests/test_todo_api.py
# Pytest test cases for the To-Do API endpoints.

import pytest
import json
from app import create_app  # Import the app factory
from app.extensions import db  # Import the db instance
from app.models.user import User
from app.models.token_blocklist import TokenBlocklist
from app.models.todo_item import TodoItem # Import the TodoItem model

# --- Test Fixtures ---

@pytest.fixture(scope='module')
def test_app_todo():
    """
    Pytest fixture to create and configure a new app instance for the To-Do test module.
    Uses the 'testing' configuration.
    """
    flask_app = create_app(config_name='testing')
    with flask_app.app_context():
        db.create_all()
        yield flask_app # Yield the app for context
        db.session.remove()
        db.drop_all()
        if hasattr(db, 'engine'): # Ensure engine attribute exists
             db.engine.dispose()


@pytest.fixture(scope='module')
def test_client_todo(test_app_todo):
    """
    Pytest fixture to provide a test client for the To-Do app.
    """
    with test_app_todo.test_client() as testing_client:
        yield testing_client


@pytest.fixture(scope='function')
def init_db_for_todos(test_app_todo): # Depends on test_app_todo for app_context
    """
    Pytest fixture to ensure a clean database for each test function.
    Clears User, TokenBlocklist, and TodoItem tables.
    """
    with test_app_todo.app_context():
        TokenBlocklist.query.delete()
        TodoItem.query.delete() # Clear TodoItems first due to potential FK to User
        User.query.delete()    # Clear Users last
        db.session.commit()
    yield


@pytest.fixture(scope='function')
def auth_headers(test_client_todo, init_db_for_todos):
    """
    Pytest fixture to register and log in a user, then return auth headers.
    """
    # Register a new user for each test function that needs auth
    test_client_todo.post('/api/v1/auth/register',
                          data=json.dumps(dict(
                              username='todo_test_user',
                              email='todo_test@example.com',
                              password='password123'
                          )),
                          content_type='application/json')

    # Log in the user
    login_response = test_client_todo.post('/api/v1/auth/login',
                                           data=json.dumps(dict(
                                               email='todo_test@example.com',
                                               password='password123'
                                           )),
                                           content_type='application/json')
    tokens = json.loads(login_response.data)
    access_token = tokens['access_token']
    return {'Authorization': f'Bearer {access_token}'}

@pytest.fixture(scope='function')
def auth_headers_user2_todo(test_client_todo, init_db_for_todos):
    """
    Pytest fixture to register and log in a second user for ownership tests in todo_api.
    """
    # Ensure the first user (from auth_headers) might exist or not, init_db_for_todos clears it.
    # Register second user
    test_client_todo.post('/api/v1/auth/register',
                          data=json.dumps(dict(
                              username='todo_test_user2',
                              email='todo_test2@example.com',
                              password='password456'
                          )),
                          content_type='application/json')
    # Login second user
    login_response = test_client_todo.post('/api/v1/auth/login',
                                           data=json.dumps(dict(
                                               email='todo_test2@example.com',
                                               password='password456'
                                           )),
                                           content_type='application/json')
    tokens = json.loads(login_response.data)
    access_token = tokens['access_token']
    return {'Authorization': f'Bearer {access_token}'}


# --- Helper function to create a todo ---
def create_todo_item_for_test(client, headers, title="Sample Todo", **kwargs):
    """Helper function to create a to-do item and return its response data."""
    payload = {"title": title, **kwargs} # Include other fields via kwargs
    response = client.post('/api/v1/todo/todos',
                           headers=headers,
                           data=json.dumps(payload),
                           content_type='application/json')
    if response.status_code != 201:
        print(f"Error creating todo item in helper: {response.status_code} - {response.data.decode()}")
        pytest.fail(f"Failed to create todo item for test setup: {response.data.decode()}")
    return json.loads(response.data)


# --- Test Cases ---

class TestTodoAPI:
    """Test suite for the To-Do API endpoints."""

    def test_get_todos_empty(self, test_client_todo, auth_headers, init_db_for_todos):
        """Test GET /todos when no to-do items exist for the user."""
        response = test_client_todo.get('/api/v1/todo/todos', headers=auth_headers)
        data = json.loads(response.data)

        assert response.status_code == 200
        assert isinstance(data, list)
        assert len(data) == 0

    def test_create_todo_minimal(self, test_client_todo, auth_headers, init_db_for_todos):
        """Test POST /todos to create a new to-do item with minimal data."""
        payload = {
            "title": "Minimal Test To-Do"
        }
        response = test_client_todo.post('/api/v1/todo/todos',
                                          headers=auth_headers,
                                          data=json.dumps(payload),
                                          content_type='application/json')
        data = json.loads(response.data)

        assert response.status_code == 201
        assert data['title'] == "Minimal Test To-Do"
        assert data['status'] == 'pending' # Default status
        assert data['priority'] == 'medium' # Default priority
        assert data['is_current_focus'] is False # Check default value
        assert 'id' in data
        assert TodoItem.query.count() == 1

    def test_create_todo_full(self, test_client_todo, auth_headers, init_db_for_todos):
        """Test POST /todos to create a new to-do item with all fields."""
        payload = {
            "title": "Full Test To-Do",
            "description": "This is a detailed description.",
            "due_date": "2025-12-01",
            "status": "in_progress",
            "priority": "high"
            # is_current_focus is not sent, should default to False
        }
        response = test_client_todo.post('/api/v1/todo/todos',
                                          headers=auth_headers,
                                          data=json.dumps(payload),
                                          content_type='application/json')
        data = json.loads(response.data)

        assert response.status_code == 201
        assert data['title'] == "Full Test To-Do"
        assert data['description'] == "This is a detailed description."
        assert data['due_date'] == "2025-12-01"
        assert data['status'] == "in_progress"
        assert data['priority'] == "high"
        assert data['is_current_focus'] is False # Check default
        assert TodoItem.query.count() == 1

    def test_get_todos_after_creation_with_focus_ordering(self, test_client_todo, auth_headers, init_db_for_todos):
        """Test GET /todos ordering with is_current_focus."""
        # Item 1 (not focus)
        create_todo_item_for_test(test_client_todo, auth_headers, title="Todo Item 1")
        # Item 2 (focus) - created later but should appear first
        todo2_data = create_todo_item_for_test(test_client_todo, auth_headers, title="Todo Item 2 (Focus)")
        # Update todo2 to be a current focus
        put_response = test_client_todo.put(f'/api/v1/todo/todos/{todo2_data["id"]}', headers=auth_headers, data=json.dumps({"is_current_focus": True}), content_type='application/json')
        assert put_response.status_code == 200 # Ensure update was successful
        # Item 3 (not focus) - created even later
        create_todo_item_for_test(test_client_todo, auth_headers, title="Todo Item 3")


        response = test_client_todo.get('/api/v1/todo/todos', headers=auth_headers)
        data = json.loads(response.data)

        assert response.status_code == 200
        assert isinstance(data, list)
        assert len(data) == 3
        assert data[0]['title'] == "Todo Item 2 (Focus)"
        assert data[0]['is_current_focus'] is True
        # The order of non-focus items depends on created_at (desc)
        assert data[1]['title'] == "Todo Item 3" # Created after Item 1
        assert data[1]['is_current_focus'] is False
        assert data[2]['title'] == "Todo Item 1"
        assert data[2]['is_current_focus'] is False


    # --- Validation and Error Tests for POST /todos ---
    def test_create_todo_missing_title(self, test_client_todo, auth_headers, init_db_for_todos):
        payload = {"description": "No title here"}
        response = test_client_todo.post('/api/v1/todo/todos', headers=auth_headers, data=json.dumps(payload), content_type='application/json')
        data = json.loads(response.data)
        assert response.status_code == 400
        assert "Title is required" in data['error']

    def test_create_todo_empty_title(self, test_client_todo, auth_headers, init_db_for_todos):
        payload = {"title": "   "} # Title with only spaces
        response = test_client_todo.post('/api/v1/todo/todos', headers=auth_headers, data=json.dumps(payload), content_type='application/json')
        data = json.loads(response.data)
        assert response.status_code == 400
        assert "Title is required and must be a non-empty string" in data['error']

    def test_create_todo_invalid_due_date_format(self, test_client_todo, auth_headers, init_db_for_todos):
        payload = {"title": "Bad Date", "due_date": "01-12-2025"} # DD-MM-YYYY format
        response = test_client_todo.post('/api/v1/todo/todos', headers=auth_headers, data=json.dumps(payload), content_type='application/json')
        data = json.loads(response.data)
        assert response.status_code == 400
        assert "Invalid due_date format" in data['error']

    def test_create_todo_invalid_status(self, test_client_todo, auth_headers, init_db_for_todos):
        payload = {"title": "Bad Status", "status": "urgent"}
        response = test_client_todo.post('/api/v1/todo/todos', headers=auth_headers, data=json.dumps(payload), content_type='application/json')
        data = json.loads(response.data)
        assert response.status_code == 400
        assert "Invalid status" in data['error']

    def test_create_todo_invalid_priority(self, test_client_todo, auth_headers, init_db_for_todos):
        payload = {"title": "Bad Priority", "priority": "critical"}
        response = test_client_todo.post('/api/v1/todo/todos', headers=auth_headers, data=json.dumps(payload), content_type='application/json')
        data = json.loads(response.data)
        assert response.status_code == 400
        assert "Invalid priority" in data['error']


    # --- Tests for GET /todos/<int:todo_id> ---
    def test_get_specific_todo_success(self, test_client_todo, auth_headers, init_db_for_todos):
        """Test successfully retrieving a specific to-do item."""
        created_todo = create_todo_item_for_test(test_client_todo, auth_headers, title="Specific Todo", description="Details")
        todo_id = created_todo['id']

        response = test_client_todo.get(f'/api/v1/todo/todos/{todo_id}', headers=auth_headers)
        data = json.loads(response.data)

        assert response.status_code == 200
        assert data['id'] == todo_id
        assert data['title'] == "Specific Todo"
        assert data['description'] == "Details"
        assert 'is_current_focus' in data # Ensure field is present
        assert data['is_current_focus'] is False # Default

    def test_get_specific_todo_not_found(self, test_client_todo, auth_headers, init_db_for_todos):
        response = test_client_todo.get('/api/v1/todo/todos/9999', headers=auth_headers)
        data = json.loads(response.data)
        assert response.status_code == 404
        assert "To-do item not found" in data['error']

    def test_get_specific_todo_not_owned(self, test_client_todo, auth_headers, auth_headers_user2_todo, init_db_for_todos):
        # User1 creates a todo
        created_todo_user1 = create_todo_item_for_test(test_client_todo, auth_headers, title="User1's Todo")
        todo_id_user1 = created_todo_user1['id']

        # User2 tries to access User1's todo
        response = test_client_todo.get(f'/api/v1/todo/todos/{todo_id_user1}', headers=auth_headers_user2_todo)
        data = json.loads(response.data)
        assert response.status_code == 403
        assert "Forbidden" in data['error']


    # --- Tests for PUT /todos/<int:todo_id> ---
    def test_update_todo_all_fields_and_focus(self, test_client_todo, auth_headers, init_db_for_todos):
        """Test successfully updating all fields of a to-do item, including is_current_focus."""
        created_todo = create_todo_item_for_test(test_client_todo, auth_headers, title="Original Title", status="pending")
        todo_id = created_todo['id']

        update_payload = {
            "title": "Updated Title",
            "description": "Now with description!",
            "status": "in_progress",
            "priority": "high",
            "due_date": "2026-01-01",
            "is_current_focus": True
        }
        response = test_client_todo.put(f'/api/v1/todo/todos/{todo_id}',
                                        headers=auth_headers,
                                        data=json.dumps(update_payload),
                                        content_type='application/json')
        data = json.loads(response.data)

        assert response.status_code == 200
        assert data['id'] == todo_id
        assert data['title'] == "Updated Title"
        assert data['description'] == "Now with description!"
        assert data['status'] == "in_progress"
        assert data['priority'] == "high"
        assert data['due_date'] == "2026-01-01"
        assert data['is_current_focus'] is True

    def test_update_todo_toggle_focus_only(self, test_client_todo, auth_headers, init_db_for_todos):
        """Test updating only the is_current_focus flag."""
        created_todo = create_todo_item_for_test(test_client_todo, auth_headers, title="Focus Toggle Test")
        todo_id = created_todo['id']
        assert created_todo['is_current_focus'] is False # Initial state

        # Set to True
        update_payload_true = {"is_current_focus": True}
        response_true = test_client_todo.put(f'/api/v1/todo/todos/{todo_id}', headers=auth_headers, data=json.dumps(update_payload_true), content_type='application/json')
        data_true = json.loads(response_true.data)
        assert response_true.status_code == 200
        assert data_true['is_current_focus'] is True

        # Set back to False
        update_payload_false = {"is_current_focus": False}
        response_false = test_client_todo.put(f'/api/v1/todo/todos/{todo_id}', headers=auth_headers, data=json.dumps(update_payload_false), content_type='application/json')
        data_false = json.loads(response_false.data)
        assert response_false.status_code == 200
        assert data_false['is_current_focus'] is False

    def test_update_todo_invalid_is_current_focus_type(self, test_client_todo, auth_headers, init_db_for_todos):
        """Test updating with invalid data type for is_current_focus."""
        created_todo = create_todo_item_for_test(test_client_todo, auth_headers, title="Bad Focus Type")
        todo_id = created_todo['id']

        update_payload = {"is_current_focus": "not-a-boolean"}
        response = test_client_todo.put(f'/api/v1/todo/todos/{todo_id}', headers=auth_headers, data=json.dumps(update_payload), content_type='application/json')
        data = json.loads(response.data)
        assert response.status_code == 400
        assert "is_current_focus must be a boolean" in data['error']
        
    def test_update_todo_not_found(self, test_client_todo, auth_headers, init_db_for_todos):
        update_payload = {"title": "Won't find me"}
        response = test_client_todo.put('/api/v1/todo/todos/9999', headers=auth_headers, data=json.dumps(update_payload), content_type='application/json')
        data = json.loads(response.data)
        assert response.status_code == 404
        assert "To-do item not found" in data['error']

    def test_update_todo_not_owned(self, test_client_todo, auth_headers, auth_headers_user2_todo, init_db_for_todos):
        created_todo_user1 = create_todo_item_for_test(test_client_todo, auth_headers, title="User1's Secret Todo")
        todo_id_user1 = created_todo_user1['id']
        update_payload = {"title": "Hacked!"}
        response = test_client_todo.put(f'/api/v1/todo/todos/{todo_id_user1}', headers=auth_headers_user2_todo, data=json.dumps(update_payload), content_type='application/json')
        data = json.loads(response.data)
        assert response.status_code == 403
        assert "Forbidden" in data['error']

    # --- Tests for DELETE /todos/<int:todo_id> ---
    def test_delete_todo_success(self, test_client_todo, auth_headers, init_db_for_todos):
        created_todo = create_todo_item_for_test(test_client_todo, auth_headers, title="To Be Deleted")
        todo_id = created_todo['id']
        assert TodoItem.query.count() == 1
        response = test_client_todo.delete(f'/api/v1/todo/todos/{todo_id}', headers=auth_headers)
        assert response.status_code == 204
        assert TodoItem.query.count() == 0
        get_response = test_client_todo.get(f'/api/v1/todo/todos/{todo_id}', headers=auth_headers)
        assert get_response.status_code == 404

    def test_delete_todo_not_found(self, test_client_todo, auth_headers, init_db_for_todos):
        response = test_client_todo.delete('/api/v1/todo/todos/9999', headers=auth_headers)
        assert response.status_code == 404

    def test_delete_todo_not_owned(self, test_client_todo, auth_headers, auth_headers_user2_todo, init_db_for_todos):
        created_todo_user1 = create_todo_item_for_test(test_client_todo, auth_headers, title="User1's Precious Todo")
        todo_id_user1 = created_todo_user1['id']
        response = test_client_todo.delete(f'/api/v1/todo/todos/{todo_id_user1}', headers=auth_headers_user2_todo)
        data = json.loads(response.data)
        assert response.status_code == 403
        assert "Forbidden" in data['error']
        assert TodoItem.query.filter_by(id=todo_id_user1).count() == 1 # Verify not deleted

    # --- Authentication Tests ---
    def test_get_todos_unauthenticated(self, test_client_todo, init_db_for_todos):
        response = test_client_todo.get('/api/v1/todo/todos')
        data = json.loads(response.data)
        assert response.status_code == 401
        assert "Missing Authorization Header" in data.get('msg', '')

    def test_create_todo_unauthenticated(self, test_client_todo, init_db_for_todos):
        payload = {"title": "Unauth Create"}
        response = test_client_todo.post('/api/v1/todo/todos', data=json.dumps(payload), content_type='application/json')
        data = json.loads(response.data)
        assert response.status_code == 401
        assert "Missing Authorization Header" in data.get('msg', '')
        
    def test_get_specific_todo_unauthenticated(self, test_client_todo, init_db_for_todos):
        response = test_client_todo.get('/api/v1/todo/todos/1')
        data = json.loads(response.data)
        assert response.status_code == 401
        assert "Missing Authorization Header" in data.get('msg', '')

    def test_update_todo_unauthenticated(self, test_client_todo, init_db_for_todos):
        response = test_client_todo.put('/api/v1/todo/todos/1', data=json.dumps({"title":"Unauth"}), content_type='application/json')
        data = json.loads(response.data)
        assert response.status_code == 401
        assert "Missing Authorization Header" in data.get('msg', '')

    def test_delete_todo_unauthenticated(self, test_client_todo, init_db_for_todos):
        response = test_client_todo.delete('/api/v1/todo/todos/1')
        data = json.loads(response.data)
        assert response.status_code == 401
        assert "Missing Authorization Header" in data.get('msg', '')
