# /your_project_root/tests/test_anchor_api.py
# Pytest test cases for the Anchor API endpoints (Profile Section).

import pytest
import json
from app import create_app  # Import the app factory
from app.extensions import db  # Import the db instance
from app.models.user import User
from app.models.user_profile import UserProfile
from app.models.token_blocklist import TokenBlocklist # For init_db_for_anchor

# --- Test Fixtures ---

@pytest.fixture(scope='module')
def test_app_anchor():
    """
    Pytest fixture to create and configure a new app instance for the Anchor test module.
    Uses the 'testing' configuration.
    """
    flask_app = create_app(config_name='testing')
    with flask_app.app_context():
        db.create_all()
        yield flask_app  # Yield the app for context
        db.session.remove()
        db.drop_all()
        if hasattr(db, 'engine'): # Ensure engine attribute exists
            db.engine.dispose()

@pytest.fixture(scope='module')
def test_client_anchor(test_app_anchor):
    """
    Pytest fixture to provide a test client for the Anchor app.
    """
    with test_app_anchor.test_client() as testing_client:
        yield testing_client

@pytest.fixture(scope='function')
def init_db_for_anchor(test_app_anchor): # Depends on test_app_anchor for app_context
    """
    Pytest fixture to ensure a clean database for each test function.
    Clears User, TokenBlocklist, and UserProfile tables.
    """
    with test_app_anchor.app_context():
        TokenBlocklist.query.delete()
        UserProfile.query.delete() # Clear UserProfiles first
        User.query.delete()        # Clear Users last
        db.session.commit()
    yield

@pytest.fixture(scope='function')
def auth_headers_anchor(test_client_anchor, init_db_for_anchor):
    """
    Pytest fixture to register and log in a user, then return auth headers
    and the user_id.
    """
    # Register a new user
    reg_response = test_client_anchor.post('/api/v1/auth/register',
                                           data=json.dumps(dict(
                                               username='anchor_test_user',
                                               email='anchor_test@example.com',
                                               password='password123'
                                           )),
                                           content_type='application/json')
    user_data = json.loads(reg_response.data)
    user_id = user_data['user']['id']

    # Log in the user
    login_response = test_client_anchor.post('/api/v1/auth/login',
                                             data=json.dumps(dict(
                                                 email='anchor_test@example.com',
                                                 password='password123'
                                             )),
                                             content_type='application/json')
    tokens = json.loads(login_response.data)
    access_token = tokens['access_token']
    
    return {'Authorization': f'Bearer {access_token}'}, user_id

# --- Test Cases ---

class TestAnchorProfileAPI:
    """Test suite for the Anchor Profile API endpoints."""

    def test_get_profile_new_user_or_auto_created(self, test_client_anchor, auth_headers_anchor, init_db_for_anchor):
        """
        Test GET /profile for a new user (profile should be auto-created or created on first GET).
        """
        headers, user_id = auth_headers_anchor
        response = test_client_anchor.get('/api/v1/anchor/profile', headers=headers)
        data = json.loads(response.data)

        assert response.status_code == 200
        assert data['user_id'] == user_id
        assert data['professional_title'] is None
        assert data['one_liner_bio'] is None
        assert 'created_at' in data
        assert 'updated_at' in data
        
        # Verify UserProfile was created in DB
        profile_in_db = UserProfile.query.filter_by(id=user_id).first()
        assert profile_in_db is not None

    def test_update_profile_success(self, test_client_anchor, auth_headers_anchor, init_db_for_anchor):
        """Test PUT /profile to successfully update profile fields."""
        headers, user_id = auth_headers_anchor

        # First GET to ensure profile exists (or is created)
        test_client_anchor.get('/api/v1/anchor/profile', headers=headers)

        update_payload = {
            "professional_title": "Software Architect",
            "one_liner_bio": "Building the future, one line of code at a time."
        }
        response = test_client_anchor.put('/api/v1/anchor/profile',
                                          headers=headers,
                                          data=json.dumps(update_payload),
                                          content_type='application/json')
        data = json.loads(response.data)

        assert response.status_code == 200
        assert data['user_id'] == user_id
        assert data['professional_title'] == "Software Architect"
        assert data['one_liner_bio'] == "Building the future, one line of code at a time."

        # Verify in DB
        profile_in_db = UserProfile.query.filter_by(id=user_id).first()
        assert profile_in_db.professional_title == "Software Architect"
        assert profile_in_db.one_liner_bio == "Building the future, one line of code at a time."

    def test_update_profile_partial_title_only(self, test_client_anchor, auth_headers_anchor, init_db_for_anchor):
        """Test PUT /profile updating only the professional title."""
        headers, user_id = auth_headers_anchor
        test_client_anchor.get('/api/v1/anchor/profile', headers=headers) # Ensure profile exists

        update_payload = {"professional_title": "Lead Developer"}
        response = test_client_anchor.put('/api/v1/anchor/profile',
                                          headers=headers,
                                          data=json.dumps(update_payload),
                                          content_type='application/json')
        data = json.loads(response.data)

        assert response.status_code == 200
        assert data['professional_title'] == "Lead Developer"
        assert data['one_liner_bio'] is None # Assuming it was null before

    def test_update_profile_partial_bio_only(self, test_client_anchor, auth_headers_anchor, init_db_for_anchor):
        """Test PUT /profile updating only the one-liner bio."""
        headers, user_id = auth_headers_anchor
        test_client_anchor.get('/api/v1/anchor/profile', headers=headers) # Ensure profile exists

        update_payload = {"one_liner_bio": "Just a dev trying to make a difference."}
        response = test_client_anchor.put('/api/v1/anchor/profile',
                                          headers=headers,
                                          data=json.dumps(update_payload),
                                          content_type='application/json')
        data = json.loads(response.data)

        assert response.status_code == 200
        assert data['professional_title'] is None # Assuming it was null before
        assert data['one_liner_bio'] == "Just a dev trying to make a difference."

    def test_update_profile_clear_fields(self, test_client_anchor, auth_headers_anchor, init_db_for_anchor):
        """Test PUT /profile to clear fields by setting them to null."""
        headers, user_id = auth_headers_anchor
        # First, set some values
        initial_payload = {"professional_title": "Initial Title", "one_liner_bio": "Initial Bio"}
        test_client_anchor.put('/api/v1/anchor/profile', headers=headers, data=json.dumps(initial_payload), content_type='application/json')

        # Now, clear them
        update_payload = {"professional_title": None, "one_liner_bio": None}
        response = test_client_anchor.put('/api/v1/anchor/profile',
                                          headers=headers,
                                          data=json.dumps(update_payload),
                                          content_type='application/json')
        data = json.loads(response.data)

        assert response.status_code == 200
        assert data['professional_title'] is None
        assert data['one_liner_bio'] is None

    def test_update_profile_no_relevant_fields(self, test_client_anchor, auth_headers_anchor, init_db_for_anchor):
        """Test PUT /profile with data but no fields that match profile schema."""
        headers, _ = auth_headers_anchor
        test_client_anchor.get('/api/v1/anchor/profile', headers=headers) # Ensure profile exists

        update_payload = {"random_field": "some_value"}
        response = test_client_anchor.put('/api/v1/anchor/profile',
                                          headers=headers,
                                          data=json.dumps(update_payload),
                                          content_type='application/json')
        data = json.loads(response.data)
        
        assert response.status_code == 200 # As per current API logic
        assert "No relevant profile fields provided for update" in data['message']


    def test_update_profile_empty_json_body(self, test_client_anchor, auth_headers_anchor, init_db_for_anchor):
        """Test PUT /profile with an empty JSON body."""
        headers, _ = auth_headers_anchor
        test_client_anchor.get('/api/v1/anchor/profile', headers=headers)

        response = test_client_anchor.put('/api/v1/anchor/profile',
                                          headers=headers,
                                          data=json.dumps({}), # Empty JSON object
                                          content_type='application/json')
        data = json.loads(response.data)
        # Corrected assertion: API returns 400 if data is an empty dict {}
        assert response.status_code == 400
        assert "Request body must be JSON and cannot be empty" in data['error']


    def test_update_profile_invalid_data_type_title(self, test_client_anchor, auth_headers_anchor, init_db_for_anchor):
        """Test PUT /profile with invalid data type for professional_title."""
        headers, _ = auth_headers_anchor
        test_client_anchor.get('/api/v1/anchor/profile', headers=headers)

        update_payload = {"professional_title": 12345} # Not a string
        response = test_client_anchor.put('/api/v1/anchor/profile',
                                          headers=headers,
                                          data=json.dumps(update_payload),
                                          content_type='application/json')
        data = json.loads(response.data)
        assert response.status_code == 400
        assert "professional_title must be a string or null" in data['error']

    def test_update_profile_invalid_data_type_bio(self, test_client_anchor, auth_headers_anchor, init_db_for_anchor):
        """Test PUT /profile with invalid data type for one_liner_bio."""
        headers, _ = auth_headers_anchor
        test_client_anchor.get('/api/v1/anchor/profile', headers=headers)

        update_payload = {"one_liner_bio": ["List", "is", "not", "string"]} # Not a string
        response = test_client_anchor.put('/api/v1/anchor/profile',
                                          headers=headers,
                                          data=json.dumps(update_payload),
                                          content_type='application/json')
        data = json.loads(response.data)
        assert response.status_code == 400
        assert "one_liner_bio must be a string or null" in data['error']

    # --- Authentication Tests ---
    def test_get_profile_unauthenticated(self, test_client_anchor, init_db_for_anchor):
        """Test GET /profile without authentication."""
        response = test_client_anchor.get('/api/v1/anchor/profile') # No auth_headers
        data = json.loads(response.data)
        assert response.status_code == 401
        assert "Missing Authorization Header" in data.get('msg', data.get('message', ''))

    def test_update_profile_unauthenticated(self, test_client_anchor, init_db_for_anchor):
        """Test PUT /profile without authentication."""
        update_payload = {"professional_title": "Unauth Update"}
        response = test_client_anchor.put('/api/v1/anchor/profile',
                                          data=json.dumps(update_payload),
                                          content_type='application/json') # No auth_headers
        data = json.loads(response.data)
        assert response.status_code == 401
        assert "Missing Authorization Header" in data.get('msg', data.get('message', ''))
