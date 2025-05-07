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
    Pytest fixture to register and log in a user, then return auth headers
    and the user_id.
    """
    # Register a new user
    reg_response = test_client_todo.post('/api/v1/auth/register',
                                        data=json.dumps(dict(
                                            username='todo_test_user',
                                            email='todo_test@example.com',
                                            password='password123'
                                        )),
                                        content_type='application/json')
    user_id = json.loads(reg_response.data)['user']['id']


    # Log in the user
    login_response = test_client_todo.post('/api/v1/auth/login',
                                           data=json.dumps(dict(
                                               email='todo_test@example.com',
                                               password='password123'
                                           )),
                                           content_type='application/json')
    tokens = json.loads(login_response.data)
    access_token = tokens['access_token']
    
    return {'Authorization': f'Bearer {access_token}'}, user_id

@pytest.fixture(scope='function')
def auth_headers_user2(test_client_todo, init_db_for_todos):
    """
    Pytest fixture to register and log in a second user for ownership tests.
    """
    test_client_todo.post('/api/v1/auth/register',
                          data=json.dumps(dict(
                              username='todo_test_user2',
                              email='todo_test2@example.com',
                              password='password456'
                          )),
                          content_type='application/json')
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
def create_todo_item(client, headers, title="Sample Todo", description=None, due_date=None, status=None, priority=None):
    """Helper function to create a to-do item and return its ID."""
    payload = {"title": title}
    if description: payload["description"] = description
    if due_date: payload["due_date"] = due_date
    if status: payload["status"] = status
    if priority: payload["priority"] = priority
    
    response = client.post('/api/v1/todo/todos',
                           headers=headers,
                           data=json.dumps(payload),
                           content_type='application/json')
    return json.loads(response.data)


# --- Test Cases ---

class TestTodoAPI:
    """Test suite for the To-Do API endpoints."""

    # Tests for GET /todos and POST /todos (from previous step)
    def test_get_todos_empty(self, test_client_todo, auth_headers, init_db_for_todos):
        """Test GET /todos when no to-do items exist for the user."""
        headers, _ = auth_headers # Unpack user_id if not needed here
        response = test_client_todo.get('/api/v1/todo/todos', headers=headers)
        data = json.loads(response.data)
        assert response.status_code == 200
        assert isinstance(data, list)
        assert len(data) == 0

    def test_create_todo_minimal(self, test_client_todo, auth_headers, init_db_for_todos):
        """Test POST /todos to create a new to-do item with minimal data."""
        headers, _ = auth_headers
        payload = {"title": "Minimal Test To-Do"}
        response = test_client_todo.post('/api/v1/todo/todos',
                                          headers=headers,
                                          data=json.dumps(payload),
                                          content_type='application/json')
        data = json.loads(response.data)
        assert response.status_code == 201
        assert data['title'] == "Minimal Test To-Do"
        assert data['status'] == 'pending'
        assert data['priority'] == 'medium'
        assert 'id' in data
        assert TodoItem.query.count() == 1

    def test_create_todo_full(self, test_client_todo, auth_headers, init_db_for_todos):
        """Test POST /todos to create a new to-do item with all fields."""
        headers, _ = auth_headers
        payload = {
            "title": "Full Test To-Do", "description": "This is a detailed description.",
            "due_date": "2025-12-01", "status": "in_progress", "priority": "high"
        }
        response = test_client_todo.post('/api/v1/todo/todos',
                                          headers=headers,
                                          data=json.dumps(payload),
                                          content_type='application/json')
        data = json.loads(response.data)
        assert response.status_code == 201
        assert data['title'] == "Full Test To-Do"
        assert data['description'] == "This is a detailed description."
        assert data['due_date'] == "2025-12-01"
        assert data['status'] == "in_progress"
        assert data['priority'] == "high"
        assert TodoItem.query.count() == 1

    def test_get_todos_after_creation(self, test_client_todo, auth_headers, init_db_for_todos):
        """Test GET /todos after creating some to-do items."""
        headers, _ = auth_headers
        create_todo_item(test_client_todo, headers, title="Todo Item 1")
        create_todo_item(test_client_todo, headers, title="Todo Item 2", priority="low")
        response = test_client_todo.get('/api/v1/todo/todos', headers=headers)
        data = json.loads(response.data)
        assert response.status_code == 200
        assert isinstance(data, list)
        assert len(data) == 2
        assert data[0]['title'] == "Todo Item 2" # Ordered by created_at desc
        assert data[1]['title'] == "Todo Item 1"

    # Validation and Error Tests for POST /todos
    def test_create_todo_missing_title(self, test_client_todo, auth_headers, init_db_for_todos):
        headers, _ = auth_headers
        payload = {"description": "No title here"}
        response = test_client_todo.post('/api/v1/todo/todos', headers=headers, data=json.dumps(payload), content_type='application/json')
        data = json.loads(response.data)
        assert response.status_code == 400
        assert "Title is required" in data['error']

    def test_create_todo_empty_title(self, test_client_todo, auth_headers, init_db_for_todos):
        headers, _ = auth_headers
        payload = {"title": "   "}
        response = test_client_todo.post('/api/v1/todo/todos', headers=headers, data=json.dumps(payload), content_type='application/json')
        data = json.loads(response.data)
        assert response.status_code == 400
        assert "Title is required and must be a non-empty string" in data['error']

    def test_create_todo_invalid_due_date_format(self, test_client_todo, auth_headers, init_db_for_todos):
        headers, _ = auth_headers
        payload = {"title": "Bad Date", "due_date": "01-12-2025"}
        response = test_client_todo.post('/api/v1/todo/todos', headers=headers, data=json.dumps(payload), content_type='application/json')
        data = json.loads(response.data)
        assert response.status_code == 400
        assert "Invalid due_date format" in data['error']

    def test_create_todo_invalid_status(self, test_client_todo, auth_headers, init_db_for_todos):
        headers, _ = auth_headers
        payload = {"title": "Bad Status", "status": "urgent"}
        response = test_client_todo.post('/api/v1/todo/todos', headers=headers, data=json.dumps(payload), content_type='application/json')
        data = json.loads(response.data)
        assert response.status_code == 400
        assert "Invalid status" in data['error']

    def test_create_todo_invalid_priority(self, test_client_todo, auth_headers, init_db_for_todos):
        headers, _ = auth_headers
        payload = {"title": "Bad Priority", "priority": "critical"}
        response = test_client_todo.post('/api/v1/todo/todos', headers=headers, data=json.dumps(payload), content_type='application/json')
        data = json.loads(response.data)
        assert response.status_code == 400
        assert "Invalid priority" in data['error']

    # --- Tests for GET /todos/<int:todo_id> ---
    def test_get_specific_todo_success(self, test_client_todo, auth_headers, init_db_for_todos):
        """Test successfully retrieving a specific to-do item."""
        headers, _ = auth_headers
        created_todo = create_todo_item(test_client_todo, headers, title="Specific Todo")
        todo_id = created_todo['id']

        response = test_client_todo.get(f'/api/v1/todo/todos/{todo_id}', headers=headers)
        data = json.loads(response.data)

        assert response.status_code == 200
        assert data['id'] == todo_id
        assert data['title'] == "Specific Todo"

    def test_get_specific_todo_not_found(self, test_client_todo, auth_headers, init_db_for_todos):
        """Test retrieving a non-existent to-do item."""
        headers, _ = auth_headers
        response = test_client_todo.get('/api/v1/todo/todos/9999', headers=headers) # Assuming 9999 doesn't exist
        data = json.loads(response.data)
        assert response.status_code == 404
        assert "To-do item not found" in data['error']

    def test_get_specific_todo_not_owned(self, test_client_todo, auth_headers, auth_headers_user2, init_db_for_todos):
        """Test retrieving a to-do item not owned by the current user."""
        headers_user1, _ = auth_headers
        headers_user2 = auth_headers_user2 # No need to unpack user_id for user2 here

        # User1 creates a todo
        created_todo_user1 = create_todo_item(test_client_todo, headers_user1, title="User1's Todo")
        todo_id_user1 = created_todo_user1['id']

        # User2 tries to access User1's todo
        response = test_client_todo.get(f'/api/v1/todo/todos/{todo_id_user1}', headers=headers_user2)
        data = json.loads(response.data)
        assert response.status_code == 403
        assert "Forbidden" in data['error']

    # --- Tests for PUT /todos/<int:todo_id> ---
    def test_update_todo_success(self, test_client_todo, auth_headers, init_db_for_todos):
        """Test successfully updating a to-do item."""
        headers, _ = auth_headers
        created_todo = create_todo_item(test_client_todo, headers, title="Original Title", status="pending")
        todo_id = created_todo['id']

        update_payload = {
            "title": "Updated Title",
            "description": "Now with description!",
            "status": "in_progress",
            "priority": "high",
            "due_date": "2026-01-01"
        }
        response = test_client_todo.put(f'/api/v1/todo/todos/{todo_id}',
                                        headers=headers,
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
        assert data['completed_at'] is None # Status is not 'completed'

    def test_update_todo_mark_completed(self, test_client_todo, auth_headers, init_db_for_todos):
        """Test updating a to-do item to 'completed' status."""
        headers, _ = auth_headers
        created_todo = create_todo_item(test_client_todo, headers, title="To Be Completed", status="pending")
        todo_id = created_todo['id']

        update_payload = {"status": "completed"}
        response = test_client_todo.put(f'/api/v1/todo/todos/{todo_id}',
                                        headers=headers,
                                        data=json.dumps(update_payload),
                                        content_type='application/json')
        data = json.loads(response.data)

        assert response.status_code == 200
        assert data['status'] == "completed"
        assert data['completed_at'] is not None # Should be set

        # Mark as incomplete again
        update_payload_2 = {"status": "pending"}
        response_2 = test_client_todo.put(f'/api/v1/todo/todos/{todo_id}',
                                        headers=headers,
                                        data=json.dumps(update_payload_2),
                                        content_type='application/json')
        data_2 = json.loads(response_2.data)
        assert response_2.status_code == 200
        assert data_2['status'] == "pending"
        assert data_2['completed_at'] is None # Should be cleared

    def test_update_todo_not_found(self, test_client_todo, auth_headers, init_db_for_todos):
        """Test updating a non-existent to-do item."""
        headers, _ = auth_headers
        update_payload = {"title": "Won't find me"}
        response = test_client_todo.put('/api/v1/todo/todos/9999',
                                        headers=headers,
                                        data=json.dumps(update_payload),
                                        content_type='application/json')
        data = json.loads(response.data)
        assert response.status_code == 404
        assert "To-do item not found" in data['error']

    def test_update_todo_not_owned(self, test_client_todo, auth_headers, auth_headers_user2, init_db_for_todos):
        """Test updating a to-do item not owned by the current user."""
        headers_user1, _ = auth_headers
        headers_user2 = auth_headers_user2

        created_todo_user1 = create_todo_item(test_client_todo, headers_user1, title="User1's Secret Todo")
        todo_id_user1 = created_todo_user1['id']

        update_payload = {"title": "Hacked!"}
        response = test_client_todo.put(f'/api/v1/todo/todos/{todo_id_user1}',
                                        headers=headers_user2, # User2 trying to update
                                        data=json.dumps(update_payload),
                                        content_type='application/json')
        data = json.loads(response.data)
        assert response.status_code == 403
        assert "Forbidden" in data['error']

    def test_update_todo_invalid_data(self, test_client_todo, auth_headers, init_db_for_todos):
        """Test updating a to-do with invalid data (e.g., bad status)."""
        headers, _ = auth_headers
        created_todo = create_todo_item(test_client_todo, headers, title="To Update Badly")
        todo_id = created_todo['id']

        update_payload = {"status": "way_too_urgent"}
        response = test_client_todo.put(f'/api/v1/todo/todos/{todo_id}',
                                        headers=headers,
                                        data=json.dumps(update_payload),
                                        content_type='application/json')
        data = json.loads(response.data)
        assert response.status_code == 400
        assert "Invalid status" in data['error']

    # --- Tests for DELETE /todos/<int:todo_id> ---
    def test_delete_todo_success(self, test_client_todo, auth_headers, init_db_for_todos):
        """Test successfully deleting a to-do item."""
        headers, _ = auth_headers
        created_todo = create_todo_item(test_client_todo, headers, title="To Be Deleted")
        todo_id = created_todo['id']

        assert TodoItem.query.count() == 1 # Verify item exists

        response = test_client_todo.delete(f'/api/v1/todo/todos/{todo_id}', headers=headers)
        
        assert response.status_code == 204 # No Content
        assert TodoItem.query.count() == 0 # Verify item is deleted from DB
        
        # Verify it's gone by trying to get it
        get_response = test_client_todo.get(f'/api/v1/todo/todos/{todo_id}', headers=headers)
        assert get_response.status_code == 404


    def test_delete_todo_not_found(self, test_client_todo, auth_headers, init_db_for_todos):
        """Test deleting a non-existent to-do item."""
        headers, _ = auth_headers
        response = test_client_todo.delete('/api/v1/todo/todos/9999', headers=headers)
        data = json.loads(response.data) # DELETE might not return JSON on 404, depends on Flask default
        assert response.status_code == 404
        # Ensure the error message is what you expect, or that it's a 404.
        # If it's a 404 from Werkzeug without a JSON body, checking 'error' in data might fail.
        # For this test, status_code == 404 is the primary check.
        # If your endpoint explicitly returns JSON for 404s:
        if response.content_type == 'application/json':
            assert "To-do item not found" in data['error']


    def test_delete_todo_not_owned(self, test_client_todo, auth_headers, auth_headers_user2, init_db_for_todos):
        """Test deleting a to-do item not owned by the current user."""
        headers_user1, _ = auth_headers
        headers_user2 = auth_headers_user2

        created_todo_user1 = create_todo_item(test_client_todo, headers_user1, title="User1's Precious Todo")
        todo_id_user1 = created_todo_user1['id']

        response = test_client_todo.delete(f'/api/v1/todo/todos/{todo_id_user1}', headers=headers_user2) # User2 trying to delete
        data = json.loads(response.data)
        assert response.status_code == 403
        assert "Forbidden" in data['error']
        assert TodoItem.query.filter_by(id=todo_id_user1).count() == 1 # Ensure item was not deleted

    # --- Authentication Tests for specific item routes ---
    def test_get_specific_todo_unauthenticated(self, test_client_todo, init_db_for_todos):
        """Test GET /todos/<id> without authentication."""
        # Need to create an item first by an authenticated user to have an ID to query
        # This setup is a bit more complex for this specific unauth test.
        # Alternatively, we can just test with an arbitrary ID.
        response = test_client_todo.get('/api/v1/todo/todos/1') # No auth_headers
        data = json.loads(response.data)
        assert response.status_code == 401
        assert "Missing Authorization Header" in data.get('msg', data.get('message', ''))

    def test_update_todo_unauthenticated(self, test_client_todo, init_db_for_todos):
        """Test PUT /todos/<id> without authentication."""
        response = test_client_todo.put('/api/v1/todo/todos/1',
                                         data=json.dumps({"title": "Unauth Update"}),
                                         content_type='application/json') # No auth_headers
        data = json.loads(response.data)
        assert response.status_code == 401
        assert "Missing Authorization Header" in data.get('msg', data.get('message', ''))

    def test_delete_todo_unauthenticated(self, test_client_todo, init_db_for_todos):
        """Test DELETE /todos/<id> without authentication."""
        response = test_client_todo.delete('/api/v1/todo/todos/1') # No auth_headers
        data = json.loads(response.data)
        assert response.status_code == 401
        assert "Missing Authorization Header" in data.get('msg', data.get('message', ''))
