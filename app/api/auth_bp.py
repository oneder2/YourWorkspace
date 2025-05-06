# /your_project_root/app/api/auth_bp.py
# Blueprint for authentication-related API endpoints (login, register, etc.).

from flask import Blueprint, jsonify, request
# Import necessary components later (e.g., User model, services, JWT functions)
# from ...models.user import User
# from ...services.auth_service import register_user, authenticate_user
# from flask_jwt_extended import create_access_token, create_refresh_token, jwt_required, get_jwt_identity

# Create a Blueprint instance named 'auth'
# The first argument 'auth' is the endpoint prefix for functions defined in this blueprint
# The second argument __name__ helps Flask locate resources
auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/ping', methods=['GET'])
def ping_auth():
    """Simple test route to check if the auth blueprint is registered and alive."""
    return jsonify({"message": "Auth API is alive!"}), 200

# --- Placeholder Routes for Authentication ---

@auth_bp.route('/register', methods=['POST'])
def register():
    """
    Endpoint for user registration.
    Expects JSON data: {'username': '...', 'email': '...', 'password': '...'}
    """
    data = request.get_json()
    if not data or not data.get('username') or not data.get('email') or not data.get('password'):
        return jsonify({"error": "Missing required fields (username, email, password)"}), 400

    # --- Add registration logic here ---
    # 1. Validate input (e.g., password complexity, email format)
    # 2. Check if username or email already exists
    # 3. Hash the password
    # 4. Create the new user in the database
    # Example (replace with actual service call):
    # try:
    #     new_user = register_user(data['username'], data['email'], data['password'])
    #     return jsonify({"message": "User registered successfully", "user_id": new_user.id}), 201
    # except ValueError as e: # Example: Catch specific errors like 'user already exists'
    #     return jsonify({"error": str(e)}), 409 # Conflict
    # except Exception as e:
    #     # Log the exception e
    #     return jsonify({"error": "Registration failed"}), 500

    # Placeholder response:
    username = data.get('username')
    return jsonify({"message": f"Placeholder: User '{username}' registration endpoint hit."}), 201


@auth_bp.route('/login', methods=['POST'])
def login():
    """
    Endpoint for user login.
    Expects JSON data: {'username': '...', 'password': '...'} or {'email': '...', 'password': '...'}
    Returns access and refresh tokens upon successful authentication.
    """
    data = request.get_json()
    if not data or not data.get('password') or not (data.get('username') or data.get('email')):
        return jsonify({"error": "Missing username/email or password"}), 400

    identifier = data.get('username') or data.get('email')
    password = data.get('password')

    # --- Add login logic here ---
    # 1. Find the user by username or email
    # 2. Verify the provided password against the stored hash
    # 3. If valid, generate JWT access and refresh tokens
    # Example (replace with actual service call):
    # user = authenticate_user(identifier, password)
    # if user:
    #     access_token = create_access_token(identity=user.id)
    #     refresh_token = create_refresh_token(identity=user.id)
    #     return jsonify(access_token=access_token, refresh_token=refresh_token), 200
    # else:
    #     return jsonify({"error": "Invalid credentials"}), 401 # Unauthorized

    # Placeholder response:
    return jsonify({
        "message": f"Placeholder: Login attempt for '{identifier}'.",
        "access_token": "placeholder_access_token",
        "refresh_token": "placeholder_refresh_token"
    }), 200


@auth_bp.route('/refresh', methods=['POST'])
#@jwt_required(refresh=True) # Requires a valid refresh token
def refresh_token():
    """
    Endpoint to obtain a new access token using a refresh token.
    Requires a valid refresh token in the Authorization header or cookie.
    """
    # --- Add token refresh logic here ---
    # 1. Get the identity from the valid refresh token
    # 2. Generate a new access token
    # Example:
    # current_user_id = get_jwt_identity()
    # new_access_token = create_access_token(identity=current_user_id)
    # return jsonify(access_token=new_access_token), 200

    # Placeholder response:
    # current_user_id = get_jwt_identity() # This would fail without @jwt_required
    current_user_id = "placeholder_user_id_from_refresh"
    return jsonify({
        "message": f"Placeholder: Token refresh for user '{current_user_id}'.",
        "access_token": "placeholder_new_access_token"
        }), 200


@auth_bp.route('/logout', methods=['POST'])
#@jwt_required() # Requires a valid access token to log out (optional, depends on strategy)
def logout():
    """
    Endpoint for user logout.
    Actual implementation depends on token handling (e.g., blocklisting).
    For simple JWT, client just needs to discard the token.
    If using blocklist: Add token JTI (JWT ID) to the blocklist.
    """
    # --- Add logout logic here (if using blocklisting) ---
    # from ...extensions import jwt_blocklist  # Assuming a blocklist set/cache
    # jti = get_jwt()['jti']
    # jwt_blocklist.add(jti)
    # return jsonify({"message": "Successfully logged out"}), 200

    # Placeholder response (if no server-side action needed):
    return jsonify({"message": "Placeholder: Logout endpoint hit. Client should discard tokens."}), 200

# You might add other auth-related routes like:
# - /profile (GET, PUT) - requires @jwt_required()
# - /change-password (POST) - requires @jwt_required()
# - /request-password-reset (POST)
# - /reset-password/<token> (POST)

