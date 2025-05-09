# /your_project_root/tests/test_auth_api.py
# Pytest test cases for the authentication API endpoints.

import pytest
import json
from app import create_app # Import the app factory
from app.extensions import db # Import the db instance
from app.models.user import User
from app.models.token_blocklist import TokenBlocklist

# --- Test Fixtures ---

@pytest.fixture(scope='module')
def test_client():
    """
    Pytest fixture to create and configure a new app instance for each test module.
    This uses the 'testing' configuration.
    """
    # Create a Flask app configured for testing
    flask_app = create_app(config_name='testing')

    # Establish an application context
    with flask_app.app_context():
        # Create all database tables
        db.create_all()

        # Create a test client using the Flask application configured for testing
        with flask_app.test_client() as testing_client:
            # Yield the test client for use in tests
            yield testing_client

        # Teardown:
        # 1. Remove the session to return connections to the pool before dropping tables
        db.session.remove()
        # 2. Drop all database tables
        db.drop_all()
        # 3. Dispose of the engine to close all connections in the pool.
        # This is important for external databases like PostgreSQL to prevent hangs.
        db.engine.dispose()


@pytest.fixture(scope='function')
def init_database(test_client): # Depends on test_client to have app_context
    """
    Pytest fixture to ensure a clean database for each test function.
    It clears data from relevant tables.
    """
    # Clear data from tables before each test
    # The order might matter if you have foreign key constraints without cascading deletes
    TokenBlocklist.query.delete()
    User.query.delete()
    db.session.commit()
    yield # Test runs here


# --- Helper Functions ---

def register_user(client, username, email, password):
    """Helper function to register a user."""
    return client.post('/api/v1/auth/register',
                       data=json.dumps(dict(
                           username=username,
                           email=email,
                           password=password
                       )),
                       content_type='application/json')

def login_user(client, email, password):
    """Helper function to log in a user."""
    return client.post('/api/v1/auth/login',
                       data=json.dumps(dict(
                           email=email,
                           password=password
                       )),
                       content_type='application/json')

# --- Test Cases ---

class TestUserRegistration:
    """Test suite for user registration functionality."""

    def test_register_success(self, test_client, init_database):
        """Test successful user registration."""
        response = register_user(test_client, 'testuser1', 'test1@example.com', 'password123')
        data = json.loads(response.data)

        assert response.status_code == 201
        assert data['message'] == 'User registered successfully'
        assert 'user' in data
        assert data['user']['username'] == 'testuser1'
        assert data['user']['email'] == 'test1@example.com'
        assert User.query.count() == 1

    def test_register_duplicate_username(self, test_client, init_database):
        """Test registration with a duplicate username."""
        register_user(test_client, 'testuser2', 'test2@example.com', 'password123')
        response = register_user(test_client, 'testuser2', 'test3@example.com', 'password456')
        data = json.loads(response.data)

        assert response.status_code == 409
        assert "Username 'testuser2' already exists" in data['error']
        assert User.query.count() == 1

    def test_register_duplicate_email(self, test_client, init_database):
        """Test registration with a duplicate email."""
        register_user(test_client, 'testuser4', 'test4@example.com', 'password123')
        response = register_user(test_client, 'testuser5', 'test4@example.com', 'password456')
        data = json.loads(response.data)

        assert response.status_code == 409
        assert "Email 'test4@example.com' already registered" in data['error']
        assert User.query.count() == 1

    def test_register_missing_fields(self, test_client, init_database):
        """Test registration with missing fields."""
        response = test_client.post('/api/v1/auth/register',
                                    data=json.dumps(dict(username='testuser6')),
                                    content_type='application/json')
        data = json.loads(response.data)

        assert response.status_code == 400
        assert 'Missing required fields' in data['error']


class TestUserLogin:
    """Test suite for user login functionality."""

    def test_login_success(self, test_client, init_database):
        """Test successful user login."""
        register_user(test_client, 'loginuser', 'login@example.com', 'password123')
        response = login_user(test_client, 'login@example.com', 'password123')
        data = json.loads(response.data)

        assert response.status_code == 200
        assert 'access_token' in data
        assert 'refresh_token' in data

    def test_login_invalid_email(self, test_client, init_database):
        """Test login with an invalid/non-existent email."""
        response = login_user(test_client, 'wrong@example.com', 'password123')
        data = json.loads(response.data)

        assert response.status_code == 401
        assert data['error'] == 'Invalid email or password'

    def test_login_incorrect_password(self, test_client, init_database):
        """Test login with an incorrect password."""
        register_user(test_client, 'loginuser2', 'login2@example.com', 'password123')
        response = login_user(test_client, 'login2@example.com', 'wrongpassword')
        data = json.loads(response.data)

        assert response.status_code == 401
        assert data['error'] == 'Invalid email or password'

    def test_login_missing_fields(self, test_client, init_database):
        """Test login with missing fields."""
        response = test_client.post('/api/v1/auth/login',
                                    data=json.dumps(dict(email='login3@example.com')),
                                    content_type='application/json')
        data = json.loads(response.data)
        assert response.status_code == 400
        assert 'Missing required fields' in data['error']


class TestProtectedRoutes:
    """Test suite for accessing protected routes and token functionality."""

    def test_access_me_route_success(self, test_client, init_database):
        """Test accessing /me with a valid access token."""
        register_user(test_client, 'protecteduser', 'protected@example.com', 'password123')
        login_response = login_user(test_client, 'protected@example.com', 'password123')
        tokens = json.loads(login_response.data)
        access_token = tokens['access_token']

        me_response = test_client.get('/api/v1/auth/me',
                                      headers={'Authorization': f'Bearer {access_token}'})
        me_data = json.loads(me_response.data)

        assert me_response.status_code == 200
        assert me_data['username'] == 'protecteduser'
        assert me_data['email'] == 'protected@example.com'

    def test_access_me_route_no_token(self, test_client, init_database):
        """Test accessing /me without an access token."""
        response = test_client.get('/api/v1/auth/me')
        data = json.loads(response.data)
        assert response.status_code == 401
        assert 'Missing Authorization Header' in data['msg']

    def test_access_me_route_invalid_token(self, test_client, init_database):
        """Test accessing /me with an invalid access token."""
        response = test_client.get('/api/v1/auth/me',
                                   headers={'Authorization': 'Bearer invalidtoken'})
        data = json.loads(response.data)
        assert response.status_code == 422
        assert 'Invalid token' in data.get('msg', '') or 'Not enough segments' in data.get('msg', '')


class TestTokenRefresh:
    """Test suite for token refresh functionality."""

    def test_refresh_token_success(self, test_client, init_database):
        """Test successfully refreshing an access token."""
        register_user(test_client, 'refreshuser', 'refresh@example.com', 'password123')
        login_response = login_user(test_client, 'refresh@example.com', 'password123')
        tokens = json.loads(login_response.data)
        refresh_token = tokens['refresh_token']

        refresh_response = test_client.post('/api/v1/auth/refresh',
                                            headers={'Authorization': f'Bearer {refresh_token}'})
        refresh_data = json.loads(refresh_response.data)

        assert refresh_response.status_code == 200
        assert 'access_token' in refresh_data

    def test_refresh_token_with_access_token(self, test_client, init_database):
        """Test attempting to refresh with an access token (should fail)."""
        register_user(test_client, 'refreshuser2', 'refresh2@example.com', 'password123')
        login_response = login_user(test_client, 'refresh2@example.com', 'password123')
        tokens = json.loads(login_response.data)
        access_token = tokens['access_token']

        refresh_response = test_client.post('/api/v1/auth/refresh',
                                            headers={'Authorization': f'Bearer {access_token}'})
        refresh_data = json.loads(refresh_response.data)

        assert refresh_response.status_code == 422 # Corrected from 401
        assert 'Only refresh tokens are allowed' in refresh_data.get('msg', '')

    def test_refresh_token_no_token(self, test_client, init_database):
        """Test attempting to refresh without any token."""
        response = test_client.post('/api/v1/auth/refresh')
        data = json.loads(response.data)
        assert response.status_code == 401
        assert 'Missing Authorization Header' in data['msg']


class TestLogoutAndBlocklist:
    """Test suite for logout and token blocklisting."""

    def test_logout_access_token_success_and_revoked(self, test_client, init_database):
        """Test successful logout and that the access token is revoked."""
        register_user(test_client, 'logoutuser', 'logout@example.com', 'password123')
        login_response = login_user(test_client, 'logout@example.com', 'password123')
        tokens = json.loads(login_response.data)
        access_token = tokens['access_token']

        logout_response = test_client.post('/api/v1/auth/logout',
                                           headers={'Authorization': f'Bearer {access_token}'})
        logout_data = json.loads(logout_response.data)

        assert logout_response.status_code == 200
        assert logout_data['message'] == 'Access token revoked. User logged out.'
        assert TokenBlocklist.query.count() == 1

        me_response = test_client.get('/api/v1/auth/me',
                                      headers={'Authorization': f'Bearer {access_token}'})
        me_data = json.loads(me_response.data)

        assert me_response.status_code == 401
        assert 'Token has been revoked' in me_data['msg']

    def test_logout_refresh_token_success_and_revoked(self, test_client, init_database):
        """Test successful logout of refresh token and that it's revoked."""
        register_user(test_client, 'logoutrefresh', 'logoutrefresh@example.com', 'password123')
        login_response = login_user(test_client, 'logoutrefresh@example.com', 'password123')
        tokens = json.loads(login_response.data)
        refresh_token = tokens['refresh_token']

        logout_refresh_response = test_client.post('/api/v1/auth/logout-refresh',
                                                   headers={'Authorization': f'Bearer {refresh_token}'})
        logout_refresh_data = json.loads(logout_refresh_response.data)

        assert logout_refresh_response.status_code == 200
        assert logout_refresh_data['message'] == 'Refresh token revoked.'
        assert TokenBlocklist.query.count() == 1

        refresh_attempt_response = test_client.post('/api/v1/auth/refresh',
                                                    headers={'Authorization': f'Bearer {refresh_token}'})
        refresh_attempt_data = json.loads(refresh_attempt_response.data)

        assert refresh_attempt_response.status_code == 401
        assert 'Token has been revoked' in refresh_attempt_data['msg']


class TestFreshTokenRequirement:
    """Test suite for routes requiring fresh tokens."""

    def test_change_password_with_fresh_token(self, test_client, init_database):
        """Test /change-password with a fresh token (directly from login)."""
        register_user(test_client, 'freshuser', 'fresh@example.com', 'password123')
        login_response = login_user(test_client, 'fresh@example.com', 'password123')
        tokens = json.loads(login_response.data)
        fresh_access_token = tokens['access_token']

        change_pass_response = test_client.post('/api/v1/auth/change-password',
                                                headers={'Authorization': f'Bearer {fresh_access_token}'},
                                                data=json.dumps(dict(new_password='newpass123')),
                                                content_type='application/json')
        change_pass_data = json.loads(change_pass_response.data)

        assert change_pass_response.status_code == 200
        assert "Password updated successfully." in change_pass_data['message']

    def test_change_password_with_non_fresh_token(self, test_client, init_database):
        """Test /change-password with a non-fresh token (from refresh)."""
        register_user(test_client, 'nonfreshuser', 'nonfresh@example.com', 'password123')
        login_response = login_user(test_client, 'nonfresh@example.com', 'password123')
        tokens = json.loads(login_response.data)
        refresh_token = tokens['refresh_token']

        refresh_response = test_client.post('/api/v1/auth/refresh',
                                            headers={'Authorization': f'Bearer {refresh_token}'})
        non_fresh_access_token = json.loads(refresh_response.data)['access_token']

        change_pass_response = test_client.post('/api/v1/auth/change-password',
                                                headers={'Authorization': f'Bearer {non_fresh_access_token}'},
                                                data=json.dumps(dict(new_password='newpass456')),
                                                content_type='application/json')
        change_pass_data = json.loads(change_pass_response.data)
        
        assert change_pass_response.status_code == 401
        assert 'Fresh token required' in change_pass_data['msg']

