#!/usr/bin/env python3
"""
API Endpoint Test Script
This script tests all the API endpoints of the Flask backend.
"""

import requests
import json
import sys
import os
import time
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

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

# Configuration
BACKEND_URL = "http://localhost:5000"
API_PREFIX = "/api/v1"

# Test user credentials
TEST_USER = {
    "username": "testuser",
    "email": "test@example.com",
    "password": "password123"
}

# Store tokens for authenticated requests
tokens = {
    "access_token": None,
    "refresh_token": None
}

def print_header(message):
    """Print a formatted header message."""
    print(f"\n{Colors.HEADER}{Colors.BOLD}{'=' * 80}{Colors.ENDC}")
    print(f"{Colors.HEADER}{Colors.BOLD}{message.center(80)}{Colors.ENDC}")
    print(f"{Colors.HEADER}{Colors.BOLD}{'=' * 80}{Colors.ENDC}\n")

def print_result(test_name, success, message=""):
    """Print a formatted test result."""
    status = f"{Colors.OKGREEN}PASS{Colors.ENDC}" if success else f"{Colors.FAIL}FAIL{Colors.ENDC}"
    print(f"{test_name.ljust(50)} [{status}] {message}")

def test_auth_endpoints():
    """Test the authentication endpoints."""
    print_header("Testing Authentication Endpoints")
    
    # Test auth ping endpoint
    try:
        response = requests.get(f"{BACKEND_URL}{API_PREFIX}/auth/ping")
        print_result("Auth ping endpoint", response.status_code == 200, 
                    f"Status: {response.status_code}, Response: {response.text}")
    except Exception as e:
        print_result("Auth ping endpoint", False, f"Error: {str(e)}")
    
    # Test login
    try:
        response = requests.post(
            f"{BACKEND_URL}{API_PREFIX}/auth/login", 
            json={"email": TEST_USER["email"], "password": TEST_USER["password"]}
        )
        
        print_result("User login", response.status_code == 200, 
                    f"Status: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            tokens["access_token"] = data.get("access_token")
            tokens["refresh_token"] = data.get("refresh_token")
            
            print_result("Access token received", tokens["access_token"] is not None)
            print_result("Refresh token received", tokens["refresh_token"] is not None)
    except Exception as e:
        print_result("User login", False, f"Error: {str(e)}")
    
    # Test authenticated endpoint
    if tokens["access_token"]:
        try:
            headers = {"Authorization": f"Bearer {tokens['access_token']}"}
            response = requests.get(f"{BACKEND_URL}{API_PREFIX}/auth/me", headers=headers)
            
            print_result("Authenticated endpoint", response.status_code == 200, 
                        f"Status: {response.status_code}")
            
            if response.status_code == 200:
                print(f"User profile: {json.dumps(response.json(), indent=2)}")
        except Exception as e:
            print_result("Authenticated endpoint", False, f"Error: {str(e)}")

def test_todo_endpoints():
    """Test the todo endpoints."""
    print_header("Testing Todo Endpoints")
    
    if not tokens["access_token"]:
        print(f"{Colors.WARNING}Skipping todo tests as no access token is available.{Colors.ENDC}")
        return
    
    headers = {"Authorization": f"Bearer {tokens['access_token']}"}
    
    # Test todo ping endpoint
    try:
        response = requests.get(f"{BACKEND_URL}{API_PREFIX}/todo/ping")
        print_result("Todo ping endpoint", response.status_code == 200, 
                    f"Status: {response.status_code}, Response: {response.text}")
    except Exception as e:
        print_result("Todo ping endpoint", False, f"Error: {str(e)}")
    
    # Test get all todos
    try:
        response = requests.get(f"{BACKEND_URL}{API_PREFIX}/todo/todos", headers=headers)
        print_result("Get all todos", response.status_code == 200, 
                    f"Status: {response.status_code}")
        
        if response.status_code == 200:
            todos = response.json()
            print(f"Found {len(todos)} todo items.")
            
            # Store the first todo ID for later tests
            if todos:
                todo_id = todos[0]["id"]
                print(f"Using todo ID {todo_id} for further tests.")
                
                # Test get todo by ID
                try:
                    response = requests.get(f"{BACKEND_URL}{API_PREFIX}/todo/todos/{todo_id}", headers=headers)
                    print_result("Get todo by ID", response.status_code == 200, 
                                f"Status: {response.status_code}")
                except Exception as e:
                    print_result("Get todo by ID", False, f"Error: {str(e)}")
    except Exception as e:
        print_result("Get all todos", False, f"Error: {str(e)}")
    
    # Test create todo
    try:
        new_todo = {
            "title": "Test todo item",
            "description": "This is a test todo item created by the API test script.",
            "status": "pending",
            "priority": "medium",
            "is_current_focus": False
        }
        
        response = requests.post(f"{BACKEND_URL}{API_PREFIX}/todo/todos", headers=headers, json=new_todo)
        print_result("Create todo", response.status_code == 201, 
                    f"Status: {response.status_code}")
        
        if response.status_code == 201:
            created_todo = response.json()
            todo_id = created_todo["id"]
            print(f"Created todo with ID {todo_id}.")
            
            # Test update todo
            try:
                update_data = {
                    "title": "Updated test todo item",
                    "status": "in_progress"
                }
                
                response = requests.put(f"{BACKEND_URL}{API_PREFIX}/todo/todos/{todo_id}", 
                                        headers=headers, json=update_data)
                print_result("Update todo", response.status_code == 200, 
                            f"Status: {response.status_code}")
            except Exception as e:
                print_result("Update todo", False, f"Error: {str(e)}")
            
            # Test delete todo
            try:
                response = requests.delete(f"{BACKEND_URL}{API_PREFIX}/todo/todos/{todo_id}", headers=headers)
                print_result("Delete todo", response.status_code == 200, 
                            f"Status: {response.status_code}")
            except Exception as e:
                print_result("Delete todo", False, f"Error: {str(e)}")
    except Exception as e:
        print_result("Create todo", False, f"Error: {str(e)}")

def test_achievements_endpoints():
    """Test the achievements endpoints."""
    print_header("Testing Achievements Endpoints")
    
    if not tokens["access_token"]:
        print(f"{Colors.WARNING}Skipping achievements tests as no access token is available.{Colors.ENDC}")
        return
    
    headers = {"Authorization": f"Bearer {tokens['access_token']}"}
    
    # Test achievements ping endpoint
    try:
        response = requests.get(f"{BACKEND_URL}{API_PREFIX}/achievements/ping")
        print_result("Achievements ping endpoint", response.status_code == 200, 
                    f"Status: {response.status_code}, Response: {response.text}")
    except Exception as e:
        print_result("Achievements ping endpoint", False, f"Error: {str(e)}")
    
    # Test get all achievements
    try:
        response = requests.get(f"{BACKEND_URL}{API_PREFIX}/achievements", headers=headers)
        print_result("Get all achievements", response.status_code == 200, 
                    f"Status: {response.status_code}")
        
        if response.status_code == 200:
            achievements = response.json()
            print(f"Found {len(achievements)} achievements.")
    except Exception as e:
        print_result("Get all achievements", False, f"Error: {str(e)}")
    
    # Test create achievement
    try:
        new_achievement = {
            "title": "Test achievement",
            "description": "This is a test achievement created by the API test script.",
            "date_achieved": "2023-05-15"
        }
        
        response = requests.post(f"{BACKEND_URL}{API_PREFIX}/achievements", headers=headers, json=new_achievement)
        print_result("Create achievement", response.status_code == 201, 
                    f"Status: {response.status_code}")
        
        if response.status_code == 201:
            created_achievement = response.json()
            achievement_id = created_achievement["id"]
            print(f"Created achievement with ID {achievement_id}.")
    except Exception as e:
        print_result("Create achievement", False, f"Error: {str(e)}")

def test_plans_endpoints():
    """Test the plans endpoints."""
    print_header("Testing Plans Endpoints")
    
    if not tokens["access_token"]:
        print(f"{Colors.WARNING}Skipping plans tests as no access token is available.{Colors.ENDC}")
        return
    
    headers = {"Authorization": f"Bearer {tokens['access_token']}"}
    
    # Test plans ping endpoint
    try:
        response = requests.get(f"{BACKEND_URL}{API_PREFIX}/plans/ping")
        print_result("Plans ping endpoint", response.status_code == 200, 
                    f"Status: {response.status_code}, Response: {response.text}")
    except Exception as e:
        print_result("Plans ping endpoint", False, f"Error: {str(e)}")
    
    # Test get all plans
    try:
        response = requests.get(f"{BACKEND_URL}{API_PREFIX}/plans", headers=headers)
        print_result("Get all plans", response.status_code == 200, 
                    f"Status: {response.status_code}")
        
        if response.status_code == 200:
            plans = response.json()
            print(f"Found {len(plans)} plans.")
    except Exception as e:
        print_result("Get all plans", False, f"Error: {str(e)}")
    
    # Test create plan
    try:
        new_plan = {
            "title": "Test future plan",
            "description": "This is a test future plan created by the API test script.",
            "goal_type": "project",
            "target_date": "2024-12-31",
            "status": "active"
        }
        
        response = requests.post(f"{BACKEND_URL}{API_PREFIX}/plans", headers=headers, json=new_plan)
        print_result("Create plan", response.status_code == 201, 
                    f"Status: {response.status_code}")
        
        if response.status_code == 201:
            created_plan = response.json()
            plan_id = created_plan["id"]
            print(f"Created plan with ID {plan_id}.")
    except Exception as e:
        print_result("Create plan", False, f"Error: {str(e)}")

def main():
    """Main function to run all tests."""
    print_header("API Endpoint Test Script")
    
    # Run all tests
    test_auth_endpoints()
    test_todo_endpoints()
    test_achievements_endpoints()
    test_plans_endpoints()
    
    print_header("Test Summary")
    print(f"{Colors.BOLD}Please review the test results above to identify any issues.{Colors.ENDC}")

if __name__ == "__main__":
    main()
