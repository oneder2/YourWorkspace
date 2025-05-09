# /your_project_root/tests/test_anchor_api.py
# Pytest test cases for the Anchor API endpoints.

import pytest
import json
from app import create_app
from app.extensions import db
from app.models.user import User
from app.models.user_profile import UserProfile
from app.models.token_blocklist import TokenBlocklist
from app.models.achievement import Achievement
# from app.models.current_focus_item import CurrentFocusItem # REMOVED
from app.models.future_plan import FuturePlan

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
        yield flask_app
        db.session.remove()
        db.drop_all()
        if hasattr(db, 'engine'):
            db.engine.dispose()

@pytest.fixture(scope='module')
def test_client_anchor(test_app_anchor):
    """
    Pytest fixture to provide a test client for the Anchor app.
    """
    with test_app_anchor.test_client() as testing_client:
        yield testing_client

@pytest.fixture(scope='function')
def init_db_for_anchor(test_app_anchor):
    """
    Pytest fixture to ensure a clean database for each test function.
    Clears User, TokenBlocklist, UserProfile, Achievement, and FuturePlan tables.
    (CurrentFocusItem related clear is removed)
    """
    with test_app_anchor.app_context():
        TokenBlocklist.query.delete()
        FuturePlan.query.delete()
        # CurrentFocusItem.query.delete() # REMOVED
        Achievement.query.delete()
        UserProfile.query.delete()
        User.query.delete()
        db.session.commit()
    yield

@pytest.fixture(scope='function')
def auth_headers_anchor(test_client_anchor, init_db_for_anchor):
    """
    Pytest fixture to register and log in a user, then return auth headers
    and the user_id.
    """
    reg_response = test_client_anchor.post('/api/v1/auth/register',
                                           data=json.dumps(dict(
                                               username='anchor_test_user',
                                               email='anchor_test@example.com',
                                               password='password123'
                                           )),
                                           content_type='application/json')
    user_data = json.loads(reg_response.data)
    user_id = user_data['user']['id']

    login_response = test_client_anchor.post('/api/v1/auth/login',
                                             data=json.dumps(dict(
                                                 email='anchor_test@example.com',
                                                 password='password123'
                                             )),
                                             content_type='application/json')
    tokens = json.loads(login_response.data)
    access_token = tokens['access_token']
    
    return {'Authorization': f'Bearer {access_token}'}, user_id

@pytest.fixture(scope='function')
def auth_headers_anchor_user2(test_client_anchor, init_db_for_anchor):
    """
    Pytest fixture to register and log in a second user for ownership tests.
    """
    # Ensure the first user (from auth_headers_anchor) might exist or not, init_db_for_anchor clears it.
    # Register second user
    test_client_anchor.post('/api/v1/auth/register',
                          data=json.dumps(dict(
                              username='anchor_test_user2',
                              email='anchor_test2@example.com',
                              password='password456'
                          )),
                          content_type='application/json')
    # Login second user
    login_response = test_client_anchor.post('/api/v1/auth/login',
                                           data=json.dumps(dict(
                                               email='anchor_test2@example.com',
                                               password='password456'
                                           )),
                                           content_type='application/json')
    tokens = json.loads(login_response.data)
    access_token = tokens['access_token']
    return {'Authorization': f'Bearer {access_token}'}


# --- Helper functions ---
def create_achievement_item(client, headers, title="Sample Achievement", **kwargs):
    """Helper function to create an achievement item and return the response data."""
    payload = {"title": title, **kwargs}
    response = client.post('/api/v1/anchor/achievements',
                           headers=headers,
                           data=json.dumps(payload),
                           content_type='application/json')
    if response.status_code != 201:
        print(f"Error creating achievement item: {response.status_code} - {response.data.decode()}")
        pytest.fail(f"Failed to create achievement item for test setup: {response.data.decode()}")
    return json.loads(response.data)

# def create_current_focus_item(client, headers, title="Sample Focus", **kwargs): # REMOVED
#     """Helper function to create a current focus item and return the response data."""
#     payload = {"title": title, **kwargs}
#     response = client.post('/api/v1/anchor/current_focus',
#                            headers=headers,
#                            data=json.dumps(payload),
#                            content_type='application/json')
#     if response.status_code != 201:
#         print(f"Error creating focus item: {response.status_code} - {response.data.decode()}")
#         pytest.fail(f"Failed to create focus item for test setup: {response.data.decode()}")
#     return json.loads(response.data)

def create_future_plan_item(client, headers, description="Sample Future Plan", **kwargs):
    """Helper function to create a future plan item and return the response data."""
    payload = {"description": description, **kwargs}
    response = client.post('/api/v1/anchor/future_plans',
                           headers=headers,
                           data=json.dumps(payload),
                           content_type='application/json')
    if response.status_code != 201:
        print(f"Error creating future plan item: {response.status_code} - {response.data.decode()}")
        pytest.fail(f"Failed to create future plan item for test setup: {response.data.decode()}")
    return json.loads(response.data)


# --- Test Cases for Profile Section ---
class TestAnchorProfileAPI:
    """Test suite for the Anchor Profile API endpoints."""
    # ... (All profile tests from previous version) ...
    def test_get_profile_new_user_or_auto_created(self, test_client_anchor, auth_headers_anchor, init_db_for_anchor):
        headers, user_id = auth_headers_anchor
        response = test_client_anchor.get('/api/v1/anchor/profile', headers=headers)
        data = json.loads(response.data)
        assert response.status_code == 200
        assert data['user_id'] == user_id
        assert data['professional_title'] is None
        assert data['one_liner_bio'] is None
        profile_in_db = UserProfile.query.filter_by(id=user_id).first()
        assert profile_in_db is not None

    def test_update_profile_success(self, test_client_anchor, auth_headers_anchor, init_db_for_anchor):
        headers, user_id = auth_headers_anchor
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
        assert data['professional_title'] == "Software Architect"
        assert data['one_liner_bio'] == "Building the future, one line of code at a time."
        profile_in_db = UserProfile.query.filter_by(id=user_id).first()
        assert profile_in_db.professional_title == "Software Architect"

    def test_update_profile_partial_title_only(self, test_client_anchor, auth_headers_anchor, init_db_for_anchor):
        headers, _ = auth_headers_anchor
        test_client_anchor.get('/api/v1/anchor/profile', headers=headers)
        update_payload = {"professional_title": "Lead Developer"}
        response = test_client_anchor.put('/api/v1/anchor/profile', headers=headers, data=json.dumps(update_payload), content_type='application/json')
        data = json.loads(response.data)
        assert response.status_code == 200
        assert data['professional_title'] == "Lead Developer"
        assert data['one_liner_bio'] is None

    def test_update_profile_partial_bio_only(self, test_client_anchor, auth_headers_anchor, init_db_for_anchor):
        headers, _ = auth_headers_anchor
        test_client_anchor.get('/api/v1/anchor/profile', headers=headers)
        update_payload = {"one_liner_bio": "Just a dev trying to make a difference."}
        response = test_client_anchor.put('/api/v1/anchor/profile', headers=headers, data=json.dumps(update_payload), content_type='application/json')
        data = json.loads(response.data)
        assert response.status_code == 200
        assert data['professional_title'] is None
        assert data['one_liner_bio'] == "Just a dev trying to make a difference."

    def test_update_profile_clear_fields(self, test_client_anchor, auth_headers_anchor, init_db_for_anchor):
        headers, _ = auth_headers_anchor
        initial_payload = {"professional_title": "Initial Title", "one_liner_bio": "Initial Bio"}
        test_client_anchor.put('/api/v1/anchor/profile', headers=headers, data=json.dumps(initial_payload), content_type='application/json')
        update_payload = {"professional_title": None, "one_liner_bio": None}
        response = test_client_anchor.put('/api/v1/anchor/profile', headers=headers, data=json.dumps(update_payload), content_type='application/json')
        data = json.loads(response.data)
        assert response.status_code == 200
        assert data['professional_title'] is None
        assert data['one_liner_bio'] is None

    def test_update_profile_no_relevant_fields(self, test_client_anchor, auth_headers_anchor, init_db_for_anchor):
        headers, _ = auth_headers_anchor
        test_client_anchor.get('/api/v1/anchor/profile', headers=headers)
        update_payload = {"random_field": "some_value"}
        response = test_client_anchor.put('/api/v1/anchor/profile', headers=headers, data=json.dumps(update_payload), content_type='application/json')
        data = json.loads(response.data)
        assert response.status_code == 200 
        assert "No relevant profile fields provided for update" in data['message']

    def test_update_profile_empty_json_body(self, test_client_anchor, auth_headers_anchor, init_db_for_anchor):
        headers, _ = auth_headers_anchor
        test_client_anchor.get('/api/v1/anchor/profile', headers=headers)
        response = test_client_anchor.put('/api/v1/anchor/profile', headers=headers, data=json.dumps({}), content_type='application/json')
        data = json.loads(response.data)
        assert response.status_code == 400
        assert "Request body must be JSON and cannot be empty" in data['error']

    def test_update_profile_invalid_data_type_title(self, test_client_anchor, auth_headers_anchor, init_db_for_anchor):
        headers, _ = auth_headers_anchor
        test_client_anchor.get('/api/v1/anchor/profile', headers=headers)
        update_payload = {"professional_title": 12345}
        response = test_client_anchor.put('/api/v1/anchor/profile', headers=headers, data=json.dumps(update_payload), content_type='application/json')
        data = json.loads(response.data)
        assert response.status_code == 400
        assert "professional_title must be a string or null" in data['error']

    def test_update_profile_invalid_data_type_bio(self, test_client_anchor, auth_headers_anchor, init_db_for_anchor):
        headers, _ = auth_headers_anchor
        test_client_anchor.get('/api/v1/anchor/profile', headers=headers)
        update_payload = {"one_liner_bio": ["List", "is", "not", "string"]}
        response = test_client_anchor.put('/api/v1/anchor/profile', headers=headers, data=json.dumps(update_payload), content_type='application/json')
        data = json.loads(response.data)
        assert response.status_code == 400
        assert "one_liner_bio must be a string or null" in data['error']

    def test_get_profile_unauthenticated(self, test_client_anchor, init_db_for_anchor):
        response = test_client_anchor.get('/api/v1/anchor/profile')
        data = json.loads(response.data)
        assert response.status_code == 401
        assert "Missing Authorization Header" in data.get('msg', '')

    def test_update_profile_unauthenticated(self, test_client_anchor, init_db_for_anchor):
        update_payload = {"professional_title": "Unauth Update"}
        response = test_client_anchor.put('/api/v1/anchor/profile', data=json.dumps(update_payload), content_type='application/json')
        data = json.loads(response.data)
        assert response.status_code == 401
        assert "Missing Authorization Header" in data.get('msg', '')


# --- Test Cases for Achievements Section ---
class TestAnchorAchievementsAPI:
    """Test suite for the Anchor Achievements API endpoints."""
    # ... (All achievement tests from previous version) ...
    def test_get_achievements_empty(self, test_client_anchor, auth_headers_anchor, init_db_for_anchor):
        headers, _ = auth_headers_anchor
        response = test_client_anchor.get('/api/v1/anchor/achievements', headers=headers)
        data = json.loads(response.data)
        assert response.status_code == 200
        assert isinstance(data, list)
        assert len(data) == 0

    def test_create_achievement_minimal(self, test_client_anchor, auth_headers_anchor, init_db_for_anchor):
        headers, user_id = auth_headers_anchor
        payload = {"title": "First Achievement"}
        response = test_client_anchor.post('/api/v1/anchor/achievements', headers=headers, data=json.dumps(payload), content_type='application/json')
        data = json.loads(response.data)
        assert response.status_code == 201
        assert data['title'] == "First Achievement"
        assert data['user_id'] == user_id
        assert data['core_skills_json'] == []
        assert Achievement.query.count() == 1

    def test_create_achievement_full(self, test_client_anchor, auth_headers_anchor, init_db_for_anchor):
        headers, user_id = auth_headers_anchor
        payload = {
            "title": "Major Project Completion", "description": "Led a team...",
            "quantifiable_results": "Saved $50k...", "core_skills_json": ["Leadership", "Python"],
            "date_achieved": "2024-01-15"
        }
        response = test_client_anchor.post('/api/v1/anchor/achievements', headers=headers, data=json.dumps(payload), content_type='application/json')
        data = json.loads(response.data)
        assert response.status_code == 201
        assert data['title'] == "Major Project Completion"
        assert data['core_skills_json'] == ["Leadership", "Python"]
        assert data['date_achieved'] == "2024-01-15"
        assert data['user_id'] == user_id
        assert Achievement.query.count() == 1

    def test_get_achievements_after_creation(self, test_client_anchor, auth_headers_anchor, init_db_for_anchor):
        headers, _ = auth_headers_anchor
        create_achievement_item(test_client_anchor, headers, title="Older Achievement", date_achieved="2023-06-01")
        create_achievement_item(test_client_anchor, headers, title="Newer Achievement", date_achieved="2024-02-01")
        create_achievement_item(test_client_anchor, headers, title="Achievement No Date")
        response = test_client_anchor.get('/api/v1/anchor/achievements', headers=headers)
        data = json.loads(response.data)
        assert response.status_code == 200
        assert len(data) == 3
        assert data[0]['title'] == "Newer Achievement"
        assert data[1]['title'] == "Older Achievement"
        assert data[2]['title'] == "Achievement No Date"

    def test_create_achievement_missing_title(self, test_client_anchor, auth_headers_anchor, init_db_for_anchor):
        headers, _ = auth_headers_anchor
        payload = {"description": "No title"}
        response = test_client_anchor.post('/api/v1/anchor/achievements', headers=headers, data=json.dumps(payload), content_type='application/json')
        data = json.loads(response.data)
        assert response.status_code == 400
        assert "Title is required" in data['error']

    def test_create_achievement_invalid_skills_format(self, test_client_anchor, auth_headers_anchor, init_db_for_anchor):
        headers, _ = auth_headers_anchor
        payload = {"title": "Bad Skills", "core_skills_json": "Python, Flask"}
        response = test_client_anchor.post('/api/v1/anchor/achievements', headers=headers, data=json.dumps(payload), content_type='application/json')
        data = json.loads(response.data)
        assert response.status_code == 400
        assert "core_skills_json must be a list" in data['error']

    def test_create_achievement_invalid_skill_in_list(self, test_client_anchor, auth_headers_anchor, init_db_for_anchor):
        headers, _ = auth_headers_anchor
        payload = {"title": "Bad Skill Item", "core_skills_json": ["Python", 123]}
        response = test_client_anchor.post('/api/v1/anchor/achievements', headers=headers, data=json.dumps(payload), content_type='application/json')
        data = json.loads(response.data)
        assert response.status_code == 400
        assert "All items in core_skills_json must be strings" in data['error']

    def test_create_achievement_invalid_date_format(self, test_client_anchor, auth_headers_anchor, init_db_for_anchor):
        headers, _ = auth_headers_anchor
        payload = {"title": "Bad Date Format", "date_achieved": "15-01-2024"}
        response = test_client_anchor.post('/api/v1/anchor/achievements', headers=headers, data=json.dumps(payload), content_type='application/json')
        data = json.loads(response.data)
        assert response.status_code == 400
        assert "Invalid date_achieved format" in data['error']

    def test_get_specific_achievement_success(self, test_client_anchor, auth_headers_anchor, init_db_for_anchor):
        headers, _ = auth_headers_anchor
        created_data = create_achievement_item(test_client_anchor, headers, title="Specific Ach", description="Details here")
        ach_id = created_data['id']
        response = test_client_anchor.get(f'/api/v1/anchor/achievements/{ach_id}', headers=headers)
        data = json.loads(response.data)
        assert response.status_code == 200
        assert data['id'] == ach_id
        assert data['title'] == "Specific Ach"

    def test_get_specific_achievement_not_found(self, test_client_anchor, auth_headers_anchor, init_db_for_anchor):
        headers, _ = auth_headers_anchor
        response = test_client_anchor.get('/api/v1/anchor/achievements/99999', headers=headers)
        data = json.loads(response.data)
        assert response.status_code == 404
        assert "Achievement not found" in data['error']

    def test_get_specific_achievement_not_owned(self, test_client_anchor, auth_headers_anchor, auth_headers_anchor_user2, init_db_for_anchor):
        headers_user1, _ = auth_headers_anchor
        headers_user2 = auth_headers_anchor_user2
        created_data_user1 = create_achievement_item(test_client_anchor, headers_user1, title="User1 Achievement")
        ach_id_user1 = created_data_user1['id']
        response = test_client_anchor.get(f'/api/v1/anchor/achievements/{ach_id_user1}', headers=headers_user2)
        data = json.loads(response.data)
        assert response.status_code == 403
        assert "Forbidden" in data['error']

    def test_update_achievement_success(self, test_client_anchor, auth_headers_anchor, init_db_for_anchor):
        headers, _ = auth_headers_anchor
        created_data = create_achievement_item(test_client_anchor, headers, title="Original Ach Title", core_skills_json=["SkillA"])
        ach_id = created_data['id']
        update_payload = { "title": "Updated Ach Title", "core_skills_json": ["SkillA", "SkillB"], "date_achieved": "2024-05-07" }
        response = test_client_anchor.put(f'/api/v1/anchor/achievements/{ach_id}', headers=headers, data=json.dumps(update_payload), content_type='application/json')
        data = json.loads(response.data)
        assert response.status_code == 200
        assert data['title'] == "Updated Ach Title"
        assert data['core_skills_json'] == ["SkillA", "SkillB"]
        assert data['date_achieved'] == "2024-05-07"

    def test_update_achievement_clear_optional_fields(self, test_client_anchor, auth_headers_anchor, init_db_for_anchor):
        headers, _ = auth_headers_anchor
        created_data = create_achievement_item(test_client_anchor, headers, title="Ach To Clear", description="Desc", date_achieved="2024-01-01", core_skills_json=["SkillC"])
        ach_id = created_data['id']
        update_payload = { "description": None, "date_achieved": None, "core_skills_json": None }
        response = test_client_anchor.put(f'/api/v1/anchor/achievements/{ach_id}', headers=headers, data=json.dumps(update_payload), content_type='application/json')
        data = json.loads(response.data)
        assert response.status_code == 200
        assert data['description'] is None
        assert data['date_achieved'] is None
        assert data['core_skills_json'] == []

    def test_update_achievement_not_found(self, test_client_anchor, auth_headers_anchor, init_db_for_anchor):
        headers, _ = auth_headers_anchor
        update_payload = {"title": "Update Non Existent"}
        response = test_client_anchor.put('/api/v1/anchor/achievements/99999', headers=headers, data=json.dumps(update_payload), content_type='application/json')
        data = json.loads(response.data)
        assert response.status_code == 404
        assert "Achievement not found" in data['error']

    def test_update_achievement_not_owned(self, test_client_anchor, auth_headers_anchor, auth_headers_anchor_user2, init_db_for_anchor):
        headers_user1, _ = auth_headers_anchor
        headers_user2 = auth_headers_anchor_user2
        created_data_user1 = create_achievement_item(test_client_anchor, headers_user1, title="User1 Ach Update")
        ach_id_user1 = created_data_user1['id']
        update_payload = {"title": "User2 Update Attempt"}
        response = test_client_anchor.put(f'/api/v1/anchor/achievements/{ach_id_user1}', headers=headers_user2, data=json.dumps(update_payload), content_type='application/json')
        data = json.loads(response.data)
        assert response.status_code == 403
        assert "Forbidden" in data['error']

    def test_update_achievement_invalid_data(self, test_client_anchor, auth_headers_anchor, init_db_for_anchor):
        headers, _ = auth_headers_anchor
        created_data = create_achievement_item(test_client_anchor, headers, title="Ach Update Invalid")
        ach_id = created_data['id']
        update_payload = {"core_skills_json": "not-a-list"}
        response = test_client_anchor.put(f'/api/v1/anchor/achievements/{ach_id}', headers=headers, data=json.dumps(update_payload), content_type='application/json')
        data = json.loads(response.data)
        assert response.status_code == 400
        assert "core_skills_json must be a list" in data['error']

    def test_delete_achievement_success(self, test_client_anchor, auth_headers_anchor, init_db_for_anchor):
        headers, _ = auth_headers_anchor
        created_data = create_achievement_item(test_client_anchor, headers, title="Ach To Delete")
        ach_id = created_data['id']
        assert Achievement.query.count() == 1
        response = test_client_anchor.delete(f'/api/v1/anchor/achievements/{ach_id}', headers=headers)
        assert response.status_code == 204
        assert Achievement.query.count() == 0
        get_response = test_client_anchor.get(f'/api/v1/anchor/achievements/{ach_id}', headers=headers)
        assert get_response.status_code == 404

    def test_delete_achievement_not_found(self, test_client_anchor, auth_headers_anchor, init_db_for_anchor):
        headers, _ = auth_headers_anchor
        response = test_client_anchor.delete('/api/v1/anchor/achievements/99999', headers=headers)
        assert response.status_code == 404

    def test_delete_achievement_not_owned(self, test_client_anchor, auth_headers_anchor, auth_headers_anchor_user2, init_db_for_anchor):
        headers_user1, _ = auth_headers_anchor
        headers_user2 = auth_headers_anchor_user2
        created_data_user1 = create_achievement_item(test_client_anchor, headers_user1, title="User1 Ach Delete")
        ach_id_user1 = created_data_user1['id']
        response = test_client_anchor.delete(f'/api/v1/anchor/achievements/{ach_id_user1}', headers=headers_user2)
        data = json.loads(response.data)
        assert response.status_code == 403
        assert "Forbidden" in data['error']
        assert Achievement.query.filter_by(id=ach_id_user1).count() == 1

    def test_get_specific_achievement_unauthenticated(self, test_client_anchor, init_db_for_anchor):
        response = test_client_anchor.get('/api/v1/anchor/achievements/1')
        data = json.loads(response.data)
        assert response.status_code == 401
        assert "Missing Authorization Header" in data.get('msg', '')

    def test_update_achievement_unauthenticated(self, test_client_anchor, init_db_for_anchor):
        response = test_client_anchor.put('/api/v1/anchor/achievements/1', data=json.dumps({"title":"Unauth"}), content_type='application/json')
        data = json.loads(response.data)
        assert response.status_code == 401
        assert "Missing Authorization Header" in data.get('msg', '')

    def test_delete_achievement_unauthenticated(self, test_client_anchor, init_db_for_anchor):
        response = test_client_anchor.delete('/api/v1/anchor/achievements/1')
        data = json.loads(response.data)
        assert response.status_code == 401
        assert "Missing Authorization Header" in data.get('msg', '')

# --- Test Cases for Future Plans Section ---
class TestAnchorFuturePlansAPI:
    """Test suite for the Anchor Future Plans API endpoints."""
    # ... (All future plans tests from previous version) ...
    def test_get_future_plans_empty(self, test_client_anchor, auth_headers_anchor, init_db_for_anchor):
        headers, _ = auth_headers_anchor
        response = test_client_anchor.get('/api/v1/anchor/future_plans', headers=headers)
        data = json.loads(response.data)
        assert response.status_code == 200
        assert isinstance(data, list)
        assert len(data) == 0

    def test_create_future_plan_minimal(self, test_client_anchor, auth_headers_anchor, init_db_for_anchor):
        headers, user_id = auth_headers_anchor
        payload = {"description": "Learn Go"}
        response = test_client_anchor.post('/api/v1/anchor/future_plans', headers=headers, data=json.dumps(payload), content_type='application/json')
        data = json.loads(response.data)
        assert response.status_code == 201
        assert data['description'] == "Learn Go"
        assert data['user_id'] == user_id
        assert data['status'] == 'active'
        assert data['goal_type'] is None
        assert FuturePlan.query.count() == 1

    def test_create_future_plan_full(self, test_client_anchor, auth_headers_anchor, init_db_for_anchor):
        headers, user_id = auth_headers_anchor
        payload = { "description": "Obtain AWS Certification", "goal_type": "certification", "target_date": "2025-11-30", "status": "active" }
        response = test_client_anchor.post('/api/v1/anchor/future_plans', headers=headers, data=json.dumps(payload), content_type='application/json')
        data = json.loads(response.data)
        assert response.status_code == 201
        assert data['description'] == "Obtain AWS Certification"
        assert data['goal_type'] == "certification"
        assert data['target_date'] == "2025-11-30"
        assert data['status'] == "active"
        assert data['user_id'] == user_id
        assert FuturePlan.query.count() == 1

    def test_get_future_plans_after_creation(self, test_client_anchor, auth_headers_anchor, init_db_for_anchor):
        headers, _ = auth_headers_anchor
        create_future_plan_item(test_client_anchor, headers, description="Plan for later", target_date="2026-06-01")
        create_future_plan_item(test_client_anchor, headers, description="Plan for sooner", target_date="2025-08-15")
        create_future_plan_item(test_client_anchor, headers, description="Plan no date")
        response = test_client_anchor.get('/api/v1/anchor/future_plans', headers=headers)
        data = json.loads(response.data)
        assert response.status_code == 200
        assert len(data) == 3
        assert data[0]['description'] == "Plan for sooner"
        assert data[1]['description'] == "Plan for later"
        assert data[2]['description'] == "Plan no date"

    def test_create_future_plan_missing_description(self, test_client_anchor, auth_headers_anchor, init_db_for_anchor):
        headers, _ = auth_headers_anchor
        payload = {"goal_type": "skill"}
        response = test_client_anchor.post('/api/v1/anchor/future_plans', headers=headers, data=json.dumps(payload), content_type='application/json')
        data = json.loads(response.data)
        assert response.status_code == 400
        assert "Description is required" in data['error']

    def test_create_future_plan_invalid_date_format(self, test_client_anchor, auth_headers_anchor, init_db_for_anchor):
        headers, _ = auth_headers_anchor
        payload = {"description": "Bad Date Plan", "target_date": "30-11-2025"}
        response = test_client_anchor.post('/api/v1/anchor/future_plans', headers=headers, data=json.dumps(payload), content_type='application/json')
        data = json.loads(response.data)
        assert response.status_code == 400
        assert "Invalid target_date format" in data['error']

    def test_create_future_plan_invalid_status(self, test_client_anchor, auth_headers_anchor, init_db_for_anchor):
        headers, _ = auth_headers_anchor
        payload = {"description": "Bad Status Plan", "status": "maybe"}
        response = test_client_anchor.post('/api/v1/anchor/future_plans', headers=headers, data=json.dumps(payload), content_type='application/json')
        data = json.loads(response.data)
        assert response.status_code == 400
        assert "Invalid status" in data['error']

    def test_get_specific_plan_success(self, test_client_anchor, auth_headers_anchor, init_db_for_anchor):
        headers, _ = auth_headers_anchor
        created_data = create_future_plan_item(test_client_anchor, headers, description="Specific Plan", goal_type="long_term")
        plan_id = created_data['id']
        response = test_client_anchor.get(f'/api/v1/anchor/future_plans/{plan_id}', headers=headers)
        data = json.loads(response.data)
        assert response.status_code == 200
        assert data['id'] == plan_id
        assert data['description'] == "Specific Plan"

    def test_get_specific_plan_not_found(self, test_client_anchor, auth_headers_anchor, init_db_for_anchor):
        headers, _ = auth_headers_anchor
        response = test_client_anchor.get('/api/v1/anchor/future_plans/99999', headers=headers)
        data = json.loads(response.data)
        assert response.status_code == 404
        assert "Future plan not found" in data['error']

    def test_get_specific_plan_not_owned(self, test_client_anchor, auth_headers_anchor, auth_headers_anchor_user2, init_db_for_anchor):
        headers_user1, _ = auth_headers_anchor
        headers_user2 = auth_headers_anchor_user2
        created_data_user1 = create_future_plan_item(test_client_anchor, headers_user1, description="User1 Plan")
        plan_id_user1 = created_data_user1['id']
        response = test_client_anchor.get(f'/api/v1/anchor/future_plans/{plan_id_user1}', headers=headers_user2)
        data = json.loads(response.data)
        assert response.status_code == 403
        assert "Forbidden" in data['error']

    def test_update_plan_success(self, test_client_anchor, auth_headers_anchor, init_db_for_anchor):
        headers, _ = auth_headers_anchor
        created_data = create_future_plan_item(test_client_anchor, headers, description="Original Plan Desc")
        plan_id = created_data['id']
        update_payload = { "description": "Updated Plan Desc", "status": "achieved", "goal_type": "short_term", "target_date": "2024-05-08" }
        response = test_client_anchor.put(f'/api/v1/anchor/future_plans/{plan_id}', headers=headers, data=json.dumps(update_payload), content_type='application/json')
        data = json.loads(response.data)
        assert response.status_code == 200
        assert data['description'] == "Updated Plan Desc"
        assert data['status'] == "achieved"
        assert data['goal_type'] == "short_term"

    def test_update_plan_clear_optional_fields(self, test_client_anchor, auth_headers_anchor, init_db_for_anchor):
        headers, _ = auth_headers_anchor
        created_data = create_future_plan_item(test_client_anchor, headers, description="Plan To Clear", goal_type="type1", target_date="2024-01-01")
        plan_id = created_data['id']
        update_payload = { "goal_type": None, "target_date": None }
        response = test_client_anchor.put(f'/api/v1/anchor/future_plans/{plan_id}', headers=headers, data=json.dumps(update_payload), content_type='application/json')
        data = json.loads(response.data)
        assert response.status_code == 200
        assert data['goal_type'] is None
        assert data['target_date'] is None

    def test_update_plan_not_found(self, test_client_anchor, auth_headers_anchor, init_db_for_anchor):
        headers, _ = auth_headers_anchor
        update_payload = {"description": "Update Non Existent Plan"}
        response = test_client_anchor.put('/api/v1/anchor/future_plans/99999', headers=headers, data=json.dumps(update_payload), content_type='application/json')
        data = json.loads(response.data)
        assert response.status_code == 404
        assert "Future plan not found" in data['error']

    def test_update_plan_not_owned(self, test_client_anchor, auth_headers_anchor, auth_headers_anchor_user2, init_db_for_anchor):
        headers_user1, _ = auth_headers_anchor
        headers_user2 = auth_headers_anchor_user2
        created_data_user1 = create_future_plan_item(test_client_anchor, headers_user1, description="User1 Plan Update")
        plan_id_user1 = created_data_user1['id']
        update_payload = {"description": "User2 Plan Update Attempt"}
        response = test_client_anchor.put(f'/api/v1/anchor/future_plans/{plan_id_user1}', headers=headers_user2, data=json.dumps(update_payload), content_type='application/json')
        data = json.loads(response.data)
        assert response.status_code == 403
        assert "Forbidden" in data['error']

    def test_update_plan_invalid_data(self, test_client_anchor, auth_headers_anchor, init_db_for_anchor):
        headers, _ = auth_headers_anchor
        created_data = create_future_plan_item(test_client_anchor, headers, description="Plan Update Invalid")
        plan_id = created_data['id']
        update_payload = {"status": "maybe"}
        response = test_client_anchor.put(f'/api/v1/anchor/future_plans/{plan_id}', headers=headers, data=json.dumps(update_payload), content_type='application/json')
        data = json.loads(response.data)
        assert response.status_code == 400
        assert "Invalid status" in data['error']

    def test_delete_plan_success(self, test_client_anchor, auth_headers_anchor, init_db_for_anchor):
        headers, _ = auth_headers_anchor
        created_data = create_future_plan_item(test_client_anchor, headers, description="Plan To Delete")
        plan_id = created_data['id']
        assert FuturePlan.query.count() == 1
        response = test_client_anchor.delete(f'/api/v1/anchor/future_plans/{plan_id}', headers=headers)
        assert response.status_code == 204
        assert FuturePlan.query.count() == 0
        get_response = test_client_anchor.get(f'/api/v1/anchor/future_plans/{plan_id}', headers=headers)
        assert get_response.status_code == 404

    def test_delete_plan_not_found(self, test_client_anchor, auth_headers_anchor, init_db_for_anchor):
        headers, _ = auth_headers_anchor
        response = test_client_anchor.delete('/api/v1/anchor/future_plans/99999', headers=headers)
        assert response.status_code == 404

    def test_delete_plan_not_owned(self, test_client_anchor, auth_headers_anchor, auth_headers_anchor_user2, init_db_for_anchor):
        headers_user1, _ = auth_headers_anchor
        headers_user2 = auth_headers_anchor_user2
        created_data_user1 = create_future_plan_item(test_client_anchor, headers_user1, description="User1 Plan Delete")
        plan_id_user1 = created_data_user1['id']
        response = test_client_anchor.delete(f'/api/v1/anchor/future_plans/{plan_id_user1}', headers=headers_user2)
        data = json.loads(response.data)
        assert response.status_code == 403
        assert "Forbidden" in data['error']
        assert FuturePlan.query.filter_by(id=plan_id_user1).count() == 1

    def test_get_specific_plan_unauthenticated(self, test_client_anchor, init_db_for_anchor):
        response = test_client_anchor.get('/api/v1/anchor/future_plans/1')
        data = json.loads(response.data)
        assert response.status_code == 401
        assert "Missing Authorization Header" in data.get('msg', '')

    def test_update_plan_unauthenticated(self, test_client_anchor, init_db_for_anchor):
        response = test_client_anchor.put('/api/v1/anchor/future_plans/1', data=json.dumps({"description":"Unauth"}), content_type='application/json')
        data = json.loads(response.data)
        assert response.status_code == 401
        assert "Missing Authorization Header" in data.get('msg', '')

    def test_delete_plan_unauthenticated(self, test_client_anchor, init_db_for_anchor):
        response = test_client_anchor.delete('/api/v1/anchor/future_plans/1')
        data = json.loads(response.data)
        assert response.status_code == 401
        assert "Missing Authorization Header" in data.get('msg', '')
