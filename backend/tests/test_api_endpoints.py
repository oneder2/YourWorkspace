#!/usr/bin/env python3
"""
API Endpoints Test Script

This script tests the backend API endpoints for achievements and plans
to ensure they are working correctly.

Usage:
1. Make sure the backend server is running on port 5000
2. Run this script: python test_api_endpoints.py
"""

import requests
import json
import sys

# Configuration
API_BASE_URL = 'http://localhost:5000/api/v1'
TEST_CREDENTIALS = {
    'email': 'test@example.com',
    'password': 'password123'
}

# Test endpoints
ENDPOINTS = {
    'login': '/auth/login',
    'achievements': '/achievements',
    'plans': '/plans'
}

# ANSI color codes for terminal output
class Colors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

def log_result(endpoint, success, message):
    """Log test result with color coding"""
    status = f"{Colors.OKGREEN}✓ PASS{Colors.ENDC}" if success else f"{Colors.FAIL}✗ FAIL{Colors.ENDC}"
    print(f"{status} - {endpoint}: {message}")

def run_tests():
    """Run all API tests"""
    print(f"{Colors.HEADER}Starting API Endpoint Tests...{Colors.ENDC}")
    print("=" * 50)
    
    access_token = None
    
    # Test 1: Login to get access token
    try:
        print(f"\n{Colors.BOLD}Testing authentication...{Colors.ENDC}")
        login_response = requests.post(
            f"{API_BASE_URL}{ENDPOINTS['login']}",
            json=TEST_CREDENTIALS,
            headers={'Content-Type': 'application/json'}
        )
        
        login_data = login_response.json()
        
        if login_response.ok and 'access_token' in login_data:
            access_token = login_data['access_token']
            log_result(ENDPOINTS['login'], True, "Successfully authenticated")
        else:
            error_msg = login_data.get('message', 'Unknown error')
            log_result(ENDPOINTS['login'], False, f"Authentication failed: {error_msg}")
            print(f"{Colors.WARNING}Cannot proceed with further tests without authentication{Colors.ENDC}")
            return 1
    except Exception as e:
        log_result(ENDPOINTS['login'], False, f"Error: {str(e)}")
        print(f"{Colors.WARNING}Cannot proceed with further tests without authentication{Colors.ENDC}")
        return 1
    
    # Test 2: Get achievements
    try:
        print(f"\n{Colors.BOLD}Testing achievements endpoint...{Colors.ENDC}")
        achievements_response = requests.get(
            f"{API_BASE_URL}{ENDPOINTS['achievements']}",
            headers={'Authorization': f"Bearer {access_token}"}
        )
        
        if achievements_response.ok:
            achievements_data = achievements_response.json()
            log_result(
                ENDPOINTS['achievements'], 
                True, 
                f"Successfully retrieved {len(achievements_data)} achievements"
            )
            # Print sample data
            if achievements_data:
                print(f"{Colors.OKBLUE}Sample data:{Colors.ENDC}")
                print(json.dumps(achievements_data[0] if achievements_data else {}, indent=2))
        else:
            try:
                error_data = achievements_response.json()
                error_msg = error_data.get('message', achievements_response.text)
            except:
                error_msg = achievements_response.text
            
            log_result(
                ENDPOINTS['achievements'], 
                False, 
                f"Failed with status {achievements_response.status_code}: {error_msg}"
            )
    except Exception as e:
        log_result(ENDPOINTS['achievements'], False, f"Error: {str(e)}")
    
    # Test 3: Get plans
    try:
        print(f"\n{Colors.BOLD}Testing plans endpoint...{Colors.ENDC}")
        plans_response = requests.get(
            f"{API_BASE_URL}{ENDPOINTS['plans']}",
            headers={'Authorization': f"Bearer {access_token}"}
        )
        
        if plans_response.ok:
            plans_data = plans_response.json()
            log_result(
                ENDPOINTS['plans'], 
                True, 
                f"Successfully retrieved {len(plans_data)} plans"
            )
            # Print sample data
            if plans_data:
                print(f"{Colors.OKBLUE}Sample data:{Colors.ENDC}")
                print(json.dumps(plans_data[0] if plans_data else {}, indent=2))
        else:
            try:
                error_data = plans_response.json()
                error_msg = error_data.get('message', plans_response.text)
            except:
                error_msg = plans_response.text
            
            log_result(
                ENDPOINTS['plans'], 
                False, 
                f"Failed with status {plans_response.status_code}: {error_msg}"
            )
    except Exception as e:
        log_result(ENDPOINTS['plans'], False, f"Error: {str(e)}")
    
    print("\n" + "=" * 50)
    print(f"{Colors.HEADER}API Endpoint Tests Completed{Colors.ENDC}")
    return 0

if __name__ == "__main__":
    sys.exit(run_tests())
