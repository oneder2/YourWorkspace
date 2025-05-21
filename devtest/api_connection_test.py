#!/usr/bin/env python3
"""
API Connection Test Script
This script tests the connectivity between the frontend and backend API.
It checks various aspects of the API configuration and connection.
"""

import requests
import json
import sys
import os
import time
import subprocess
import signal
from urllib.parse import urlparse

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
FRONTEND_URL = "http://localhost:5173"
API_PREFIX = "/api/v1"

# Test user credentials
TEST_USER = {
    "username": "testuser123",
    "email": "testuser123@example.com",
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

def check_server_running(url, name):
    """Check if a server is running at the given URL."""
    try:
        response = requests.get(url, timeout=2)
        return True, response.status_code
    except requests.exceptions.ConnectionError:
        return False, None
    except Exception as e:
        return False, str(e)

def test_backend_connection():
    """Test the connection to the backend server."""
    print_header("Testing Backend Connection")
    
    # Check if backend is running
    is_running, status = check_server_running(BACKEND_URL, "Backend")
    print_result("Backend server running", is_running, f"Status: {status}")
    
    if not is_running:
        print(f"{Colors.WARNING}Backend server is not running. Please start it first.{Colors.ENDC}")
        return False
    
    # Test root endpoint
    try:
        response = requests.get(BACKEND_URL)
        print_result("Backend root endpoint", response.status_code == 200, 
                    f"Status: {response.status_code}, Response: {response.text}")
    except Exception as e:
        print_result("Backend root endpoint", False, f"Error: {str(e)}")
    
    return is_running

def test_cors_configuration():
    """Test the CORS configuration of the backend."""
    print_header("Testing CORS Configuration")
    
    # Test preflight request
    try:
        headers = {
            'Origin': FRONTEND_URL,
            'Access-Control-Request-Method': 'GET',
            'Access-Control-Request-Headers': 'Content-Type, Authorization'
        }
        response = requests.options(f"{BACKEND_URL}{API_PREFIX}/auth/ping", headers=headers)
        
        cors_headers = response.headers.get('Access-Control-Allow-Origin')
        methods_header = response.headers.get('Access-Control-Allow-Methods')
        
        print_result("CORS preflight response", response.status_code < 400, 
                    f"Status: {response.status_code}")
        print_result("Access-Control-Allow-Origin header", cors_headers is not None, 
                    f"Value: {cors_headers}")
        print_result("Access-Control-Allow-Methods header", methods_header is not None, 
                    f"Value: {methods_header}")
        
    except Exception as e:
        print_result("CORS preflight request", False, f"Error: {str(e)}")

def test_api_endpoints():
    """Test various API endpoints."""
    print_header("Testing API Endpoints")
    
    # Test auth ping endpoint
    try:
        response = requests.get(f"{BACKEND_URL}{API_PREFIX}/auth/ping")
        print_result("Auth ping endpoint", response.status_code == 200, 
                    f"Status: {response.status_code}, Response: {response.text}")
    except Exception as e:
        print_result("Auth ping endpoint", False, f"Error: {str(e)}")
    
    # Test todo ping endpoint
    try:
        response = requests.get(f"{BACKEND_URL}{API_PREFIX}/todo/ping")
        print_result("Todo ping endpoint", response.status_code == 200, 
                    f"Status: {response.status_code}, Response: {response.text}")
    except Exception as e:
        print_result("Todo ping endpoint", False, f"Error: {str(e)}")
    
    # Test achievements ping endpoint (if it exists)
    try:
        response = requests.get(f"{BACKEND_URL}{API_PREFIX}/achievements/ping")
        print_result("Achievements ping endpoint", response.status_code == 200, 
                    f"Status: {response.status_code}, Response: {response.text}")
    except Exception as e:
        print_result("Achievements ping endpoint", False, f"Error: {str(e)}")
    
    # Test plans ping endpoint (if it exists)
    try:
        response = requests.get(f"{BACKEND_URL}{API_PREFIX}/plans/ping")
        print_result("Plans ping endpoint", response.status_code == 200, 
                    f"Status: {response.status_code}, Response: {response.text}")
    except Exception as e:
        print_result("Plans ping endpoint", False, f"Error: {str(e)}")

def test_auth_flow():
    """Test the authentication flow."""
    print_header("Testing Authentication Flow")
    
    # Test registration
    try:
        response = requests.post(
            f"{BACKEND_URL}{API_PREFIX}/auth/register", 
            json=TEST_USER
        )
        
        if response.status_code == 409:
            print_result("User registration", True, "User already exists (409)")
        else:
            print_result("User registration", response.status_code == 201, 
                        f"Status: {response.status_code}, Response: {response.text}")
    except Exception as e:
        print_result("User registration", False, f"Error: {str(e)}")
    
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

def check_database_config():
    """Check the database configuration."""
    print_header("Checking Database Configuration")
    
    # Check if using SQLite or PostgreSQL
    try:
        with open("backend/.env", "r") as f:
            env_content = f.read()
            
        if "sqlite" in env_content.lower():
            print_result("Database type", True, "Using SQLite")
            
            # Check if SQLite file exists
            sqlite_path = None
            for line in env_content.split("\n"):
                if "sqlite" in line.lower() and "=" in line:
                    path_part = line.split("=")[1].strip().strip("'").strip('"')
                    if "sqlite:///" in path_part:
                        sqlite_path = path_part.replace("sqlite:///", "")
            
            if sqlite_path:
                exists = os.path.exists(sqlite_path)
                print_result("SQLite database file exists", exists, f"Path: {sqlite_path}")
            else:
                print_result("SQLite database path", False, "Could not determine path")
        
        elif "postgresql" in env_content.lower() or "postgres" in env_content.lower():
            print_result("Database type", True, "Using PostgreSQL")
            
            # Extract PostgreSQL connection details
            pg_host = None
            pg_port = None
            pg_user = None
            pg_db = None
            
            for line in env_content.split("\n"):
                if "POSTGRES_HOST" in line and "=" in line:
                    pg_host = line.split("=")[1].strip().strip("'").strip('"')
                elif "POSTGRES_PORT" in line and "=" in line:
                    pg_port = line.split("=")[1].strip().strip("'").strip('"')
                elif "POSTGRES_USER" in line and "=" in line:
                    pg_user = line.split("=")[1].strip().strip("'").strip('"')
                elif "POSTGRES_DB_DEV" in line and "=" in line:
                    pg_db = line.split("=")[1].strip().strip("'").strip('"')
            
            print(f"PostgreSQL connection: {pg_user}@{pg_host}:{pg_port}/{pg_db}")
            
            # We can't easily test PostgreSQL connection without password
            print(f"{Colors.WARNING}Note: Cannot fully verify PostgreSQL connection without password{Colors.ENDC}")
        
        else:
            print_result("Database type", False, "Could not determine database type")
    
    except Exception as e:
        print_result("Database configuration check", False, f"Error: {str(e)}")

def check_frontend_api_config():
    """Check the frontend API configuration."""
    print_header("Checking Frontend API Configuration")
    
    try:
        with open("svelte@latest/.env", "r") as f:
            env_content = f.read()
            
        api_base_url = None
        for line in env_content.split("\n"):
            if "VITE_API_BASE_URL" in line and "=" in line:
                api_base_url = line.split("=")[1].strip().strip("'").strip('"')
        
        if api_base_url:
            print_result("Frontend API base URL", True, f"Value: {api_base_url}")
            
            # Check if it's a relative or absolute URL
            is_absolute = bool(urlparse(api_base_url).netloc)
            print_result("URL type", True, "Absolute" if is_absolute else "Relative")
            
            if is_absolute:
                # For absolute URLs, check if the host is reachable
                host = urlparse(api_base_url).netloc
                print(f"Checking if host '{host}' is reachable...")
                # This is a simple check and might not work for all cases
                is_running, status = check_server_running(f"http://{host}", "API host")
                print_result("API host reachable", is_running, f"Status: {status}")
            else:
                # For relative URLs, check if it matches the backend API prefix
                matches_backend = api_base_url == API_PREFIX
                print_result("Matches backend API prefix", matches_backend, 
                            f"Frontend: {api_base_url}, Backend: {API_PREFIX}")
        else:
            print_result("Frontend API base URL", False, "Not found in .env file")
    
    except Exception as e:
        print_result("Frontend API configuration check", False, f"Error: {str(e)}")

def check_vite_proxy_config():
    """Check the Vite proxy configuration."""
    print_header("Checking Vite Proxy Configuration")
    
    try:
        with open("svelte@latest/vite.config.ts", "r") as f:
            config_content = f.read()
            
        if "proxy" in config_content:
            proxy_section = config_content.split("proxy")[1].split("{")[1].split("}")[0]
            print_result("Vite proxy configuration", True, "Found in vite.config.ts")
            print(f"Proxy configuration:\n{proxy_section}")
            
            # Check if proxy is commented out
            if "// proxy" in config_content or "//proxy" in config_content:
                print_result("Proxy status", False, "Proxy configuration is commented out")
            else:
                print_result("Proxy status", True, "Proxy configuration is active")
        else:
            print_result("Vite proxy configuration", False, "Not found in vite.config.ts")
            print(f"{Colors.WARNING}Consider adding a proxy configuration to vite.config.ts{Colors.ENDC}")
    
    except Exception as e:
        print_result("Vite proxy configuration check", False, f"Error: {str(e)}")

def main():
    """Main function to run all tests."""
    print_header("API Connection Test Script")
    
    # Check if backend is running
    backend_running = test_backend_connection()
    if not backend_running:
        print(f"{Colors.WARNING}Skipping further tests as backend is not running.{Colors.ENDC}")
        return
    
    # Run all tests
    test_cors_configuration()
    test_api_endpoints()
    test_auth_flow()
    check_database_config()
    check_frontend_api_config()
    check_vite_proxy_config()
    
    print_header("Test Summary")
    print(f"{Colors.BOLD}Please review the test results above to identify any issues.{Colors.ENDC}")
    print(f"{Colors.BOLD}Common issues include:{Colors.ENDC}")
    print(f"1. {Colors.WARNING}CORS configuration{Colors.ENDC} - Backend needs to allow requests from frontend")
    print(f"2. {Colors.WARNING}API URL mismatch{Colors.ENDC} - Frontend and backend API paths don't match")
    print(f"3. {Colors.WARNING}Database connection{Colors.ENDC} - Backend can't connect to the database")
    print(f"4. {Colors.WARNING}Missing proxy{Colors.ENDC} - Frontend needs a proxy for API requests in development")

if __name__ == "__main__":
    main()
