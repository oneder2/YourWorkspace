#!/usr/bin/env python3
"""
API Testing Script for Flask Backend
This script tests the various API endpoints of the Flask backend.
"""

import requests
import json
import sys
import threading
import time
from pprint import pprint
from app import create_app

# Start the Flask server in a separate thread
def start_flask_server():
    app = create_app('testing')
    app.run(host='localhost', port=5000, debug=False)

# Start the server in a separate thread
server_thread = threading.Thread(target=start_flask_server)
server_thread.daemon = True
server_thread.start()

# Wait for the server to start
print("Starting Flask server...")
time.sleep(2)
print("Server should be running now.")

# Base URL for the API
BASE_URL = "http://localhost:5000/api/v1"

# Store tokens for authenticated requests
tokens = {
    "access_token": None,
    "refresh_token": None
}

# Test user credentials
TEST_USER = {
    "username": "testuser123",
    "email": "testuser123@example.com",
    "password": "password123"
}

# Colors for terminal output
class Colors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

def print_section(title):
    """Print a section title."""
    print(f"\n{Colors.HEADER}{Colors.BOLD}{'=' * 50}{Colors.ENDC}")
    print(f"{Colors.HEADER}{Colors.BOLD}{title.center(50)}{Colors.ENDC}")
    print(f"{Colors.HEADER}{Colors.BOLD}{'=' * 50}{Colors.ENDC}\n")

def print_test(name, success, response=None, error=None):
    """Print the result of a test."""
    if success:
        print(f"{Colors.OKGREEN}✓ {name}{Colors.ENDC}")
        if response:
            print(f"  Response: {response}")
    else:
        print(f"{Colors.FAIL}✗ {name}{Colors.ENDC}")
        if error:
            print(f"  Error: {error}")
        if response:
            print(f"  Response: {response}")

def get_auth_headers():
    """Return headers with authorization token."""
    if not tokens["access_token"]:
        print(f"{Colors.WARNING}Warning: No access token available{Colors.ENDC}")
        return {}
    return {"Authorization": f"Bearer {tokens['access_token']}"}

def test_auth_api():
    """Test the Authentication API endpoints."""
    print_section("Testing Authentication API")

    # Test ping endpoint
    try:
        response = requests.get(f"{BASE_URL}/auth/ping")
        print_test("Auth Ping", response.status_code == 200, response.json())
    except Exception as e:
        print_test("Auth Ping", False, error=str(e))
        return False

    # Test registration
    try:
        # First, try to register the test user
        response = requests.post(
            f"{BASE_URL}/auth/register",
            json=TEST_USER
        )

        # If user already exists, that's fine
        if response.status_code == 409:
            print_test("User Registration (User already exists)", True)
        else:
            print_test("User Registration", response.status_code == 201, response.json())
    except Exception as e:
        print_test("User Registration", False, error=str(e))
        return False

    # Test login
    try:
        response = requests.post(
            f"{BASE_URL}/auth/login",
            json={
                "email": TEST_USER["email"],
                "password": TEST_USER["password"]
            }
        )

        if response.status_code == 200:
            tokens["access_token"] = response.json().get("access_token")
            tokens["refresh_token"] = response.json().get("refresh_token")
            print_test("User Login", True, "Tokens received")
        else:
            print_test("User Login", False, response.json())
            return False
    except Exception as e:
        print_test("User Login", False, error=str(e))
        return False

    # Test /me endpoint
    try:
        response = requests.get(
            f"{BASE_URL}/auth/me",
            headers=get_auth_headers()
        )
        print_test("Get Current User", response.status_code == 200, response.json())
    except Exception as e:
        print_test("Get Current User", False, error=str(e))

    return True

def test_profile_api():
    """Test the Profile API endpoints."""
    print_section("Testing Profile API")

    # Test ping endpoint
    try:
        response = requests.get(f"{BASE_URL}/anchor/ping")
        print_test("Profile Ping", response.status_code == 200, response.json())
    except Exception as e:
        print_test("Profile Ping", False, error=str(e))
        return False

    # Test get profile
    try:
        response = requests.get(
            f"{BASE_URL}/anchor/profile",
            headers=get_auth_headers()
        )
        print_test("Get Profile", response.status_code == 200, response.json())
    except Exception as e:
        print_test("Get Profile", False, error=str(e))
        return False

    # Test update profile
    try:
        profile_data = {
            "professional_title": "Software Engineer",
            "one_liner_bio": "Building amazing software",
            "skill": "Python, Flask, Svelte",
            "summary": "Experienced software engineer with a passion for building web applications."
        }

        response = requests.put(
            f"{BASE_URL}/anchor/profile",
            headers=get_auth_headers(),
            json=profile_data
        )
        print_test("Update Profile", response.status_code == 200, response.json())
    except Exception as e:
        print_test("Update Profile", False, error=str(e))

    return True

def test_achievements_api():
    """Test the Achievements API endpoints."""
    print_section("Testing Achievements API")

    # Test ping endpoint
    try:
        response = requests.get(f"{BASE_URL}/achievements/ping")
        print_test("Achievements Ping", response.status_code == 200, response.json())
    except Exception as e:
        print_test("Achievements Ping", False, error=str(e))
        return False

    # Test create achievement
    achievement_id = None
    try:
        achievement_data = {
            "title": "Completed API Testing",
            "description": "Successfully tested all API endpoints",
            "quantifiable_results": "100% test coverage",
            "core_skills_json": ["Python", "API Testing", "Flask"],
            "date_achieved": "2024-05-15"
        }

        response = requests.post(
            f"{BASE_URL}/achievements/",
            headers=get_auth_headers(),
            json=achievement_data
        )

        if response.status_code == 201:
            achievement_id = response.json().get("id")
            print_test("Create Achievement", True, response.json())
        else:
            print_test("Create Achievement", False, response.json())
            return False
    except Exception as e:
        print_test("Create Achievement", False, error=str(e))
        return False

    # Test get all achievements
    try:
        response = requests.get(
            f"{BASE_URL}/achievements/",
            headers=get_auth_headers()
        )
        print_test("Get All Achievements", response.status_code == 200, f"Found {len(response.json())} achievements")
    except Exception as e:
        print_test("Get All Achievements", False, error=str(e))

    # Test get achievement by ID
    if achievement_id:
        try:
            response = requests.get(
                f"{BASE_URL}/achievements/{achievement_id}",
                headers=get_auth_headers()
            )
            print_test("Get Achievement by ID", response.status_code == 200, response.json())
        except Exception as e:
            print_test("Get Achievement by ID", False, error=str(e))

    # Test update achievement
    if achievement_id:
        try:
            update_data = {
                "title": "Updated Achievement Title",
                "core_skills_json": ["Python", "API Testing", "Flask", "Documentation"]
            }

            response = requests.put(
                f"{BASE_URL}/achievements/{achievement_id}",
                headers=get_auth_headers(),
                json=update_data
            )
            print_test("Update Achievement", response.status_code == 200, response.json())
        except Exception as e:
            print_test("Update Achievement", False, error=str(e))

    # Test delete achievement
    if achievement_id:
        try:
            response = requests.delete(
                f"{BASE_URL}/achievements/{achievement_id}",
                headers=get_auth_headers()
            )
            print_test("Delete Achievement", response.status_code == 204, "Achievement deleted")
        except Exception as e:
            print_test("Delete Achievement", False, error=str(e))

    return True

def test_plans_api():
    """Test the Plans API endpoints."""
    print_section("Testing Plans API")

    # Test ping endpoint
    try:
        response = requests.get(f"{BASE_URL}/plans/ping")
        print_test("Plans Ping", response.status_code == 200, response.json())
    except Exception as e:
        print_test("Plans Ping", False, error=str(e))
        return False

    # Test create plan
    plan_id = None
    try:
        plan_data = {
            "title": "Learn AI Technology",
            "description": "Study machine learning and deep learning fundamentals",
            "goal_type": "Learning",
            "status": "active",
            "target_date": "2026-12-31"
        }

        response = requests.post(
            f"{BASE_URL}/plans/",
            headers=get_auth_headers(),
            json=plan_data
        )

        if response.status_code == 201:
            plan_id = response.json().get("id")
            print_test("Create Plan", True, response.json())
        else:
            print_test("Create Plan", False, response.json())
            return False
    except Exception as e:
        print_test("Create Plan", False, error=str(e))
        return False

    # Test get all plans
    try:
        response = requests.get(
            f"{BASE_URL}/plans/",
            headers=get_auth_headers()
        )
        print_test("Get All Plans", response.status_code == 200, f"Found {len(response.json())} plans")
    except Exception as e:
        print_test("Get All Plans", False, error=str(e))

    # Test get plan by ID
    if plan_id:
        try:
            response = requests.get(
                f"{BASE_URL}/plans/{plan_id}",
                headers=get_auth_headers()
            )
            print_test("Get Plan by ID", response.status_code == 200, response.json())
        except Exception as e:
            print_test("Get Plan by ID", False, error=str(e))

    # Test update plan
    if plan_id:
        try:
            update_data = {
                "title": "Updated Plan Title",
                "status": "active"  # Valid status values: 'active', 'achieved', 'deferred', 'abandoned'
            }

            response = requests.put(
                f"{BASE_URL}/plans/{plan_id}",
                headers=get_auth_headers(),
                json=update_data
            )
            print_test("Update Plan", response.status_code == 200, response.json())
        except Exception as e:
            print_test("Update Plan", False, error=str(e))

    # Test delete plan
    if plan_id:
        try:
            response = requests.delete(
                f"{BASE_URL}/plans/{plan_id}",
                headers=get_auth_headers()
            )
            print_test("Delete Plan", response.status_code == 204, "Plan deleted")
        except Exception as e:
            print_test("Delete Plan", False, error=str(e))

    return True

def test_todo_api():
    """Test the Todo API endpoints."""
    print_section("Testing Todo API")

    # Test ping endpoint
    try:
        response = requests.get(f"{BASE_URL}/todo/ping")
        print_test("Todo Ping", response.status_code == 200, response.json())
    except Exception as e:
        print_test("Todo Ping", False, error=str(e))
        return False

    # Test create todo
    todo_id = None
    try:
        todo_data = {
            "title": "Complete API Documentation",
            "description": "Finish documenting all API endpoints",
            "due_date": "2024-06-30",
            "status": "pending",
            "priority": "high"
        }

        response = requests.post(
            f"{BASE_URL}/todo/todos",
            headers=get_auth_headers(),
            json=todo_data
        )

        if response.status_code == 201:
            todo_id = response.json().get("id")
            print_test("Create Todo", True, response.json())
        else:
            print_test("Create Todo", False, response.json())
            return False
    except Exception as e:
        print_test("Create Todo", False, error=str(e))
        return False

    # Test get all todos
    try:
        response = requests.get(
            f"{BASE_URL}/todo/todos",
            headers=get_auth_headers()
        )
        print_test("Get All Todos", response.status_code == 200, f"Found {len(response.json())} todos")
    except Exception as e:
        print_test("Get All Todos", False, error=str(e))

    # Test get todo by ID
    if todo_id:
        try:
            response = requests.get(
                f"{BASE_URL}/todo/todos/{todo_id}",
                headers=get_auth_headers()
            )
            print_test("Get Todo by ID", response.status_code == 200, response.json())
        except Exception as e:
            print_test("Get Todo by ID", False, error=str(e))

    # Test update todo
    if todo_id:
        try:
            update_data = {
                "title": "Updated Todo Title",
                "status": "in_progress",
                "is_current_focus": True
            }

            response = requests.put(
                f"{BASE_URL}/todo/todos/{todo_id}",
                headers=get_auth_headers(),
                json=update_data
            )
            print_test("Update Todo", response.status_code == 200, response.json())
        except Exception as e:
            print_test("Update Todo", False, error=str(e))

    # Test delete todo
    if todo_id:
        try:
            response = requests.delete(
                f"{BASE_URL}/todo/todos/{todo_id}",
                headers=get_auth_headers()
            )
            print_test("Delete Todo", response.status_code == 204, "Todo deleted")
        except Exception as e:
            print_test("Delete Todo", False, error=str(e))

    return True

def test_blog_api():
    """Test the Blog API endpoints."""
    print_section("Testing Blog API")

    # Test ping endpoint
    try:
        response = requests.get(f"{BASE_URL}/blog/ping")
        print_test("Blog Ping", response.status_code == 200, response.json())
    except Exception as e:
        print_test("Blog Ping", False, error=str(e))
        return False

    return True

def test_ai_api():
    """Test the AI API endpoints."""
    print_section("Testing AI API")

    # Test ping endpoint
    try:
        response = requests.get(f"{BASE_URL}/ai/ping")
        print_test("AI Ping", response.status_code == 200, response.json())
    except Exception as e:
        print_test("AI Ping", False, error=str(e))
        return False

    return True

def main():
    """Main function to run all tests."""
    print_section("API Testing Script")

    # Test Authentication API (required for other tests)
    if not test_auth_api():
        print(f"{Colors.FAIL}Authentication API tests failed. Cannot proceed with other tests.{Colors.ENDC}")
        return

    # Test other APIs
    test_profile_api()
    test_achievements_api()
    test_plans_api()
    test_todo_api()
    test_blog_api()
    test_ai_api()

    print_section("Testing Complete")

if __name__ == "__main__":
    main()
