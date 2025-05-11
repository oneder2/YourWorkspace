import requests
import json

# Login to get a token
login_data = {
    "email": "testuser2@example.com",
    "password": "password123"
}

response = requests.post("http://127.0.0.1:5000/api/v1/auth/login", json=login_data)
print("Login response:", response.status_code)
print(response.json())

if response.status_code == 200:
    token_data = response.json()
    access_token = token_data.get("access_token")

    # Test the profile endpoint
    headers = {
        "Authorization": f"Bearer {access_token}"
    }

    profile_response = requests.get("http://127.0.0.1:5000/api/v1/anchor/profile", headers=headers)
    print("\nProfile response:", profile_response.status_code)
    print(json.dumps(profile_response.json(), indent=2))

    # Test the achievements endpoint
    achievements_response = requests.get("http://127.0.0.1:5000/api/v1/anchor/achievements", headers=headers)
    print("\nAchievements response:", achievements_response.status_code)
    print(json.dumps(achievements_response.json(), indent=2))
