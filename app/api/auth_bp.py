# /your_project_root/app/api/auth_bp.py
# Blueprint for authentication-related API endpoints (login, register, etc.).

from flask import Blueprint, jsonify, request
from sqlalchemy.exc import IntegrityError # To catch unique constraint violations

# Import database session, User model, and bcrypt instance
from ..extensions import db, bcrypt
from ..models.user import User # Import the User model

# Import JWT functions later when implementing login
from flask_jwt_extended import create_access_token, create_refresh_token, jwt_required, get_jwt_identity

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/ping', methods=['GET'])
def ping_auth():
    """Simple test route."""
    return jsonify({"message": "Auth API is alive!"}), 200


@auth_bp.route('/register', methods=['POST'])
def register():
    """Handles user registration."""
    # 1. Get data from the incoming JSON request
    data = request.get_json()
    if not data:
        return jsonify({"error": "Request body must be JSON"}), 400

    username = data.get('username')
    email = data.get('email')
    password = data.get('password')

    # 2. Basic Input Validation
    if not username or not email or not password:
        return jsonify({"error": "Missing required fields (username, email, password)"}), 400

    # Add more specific validation if needed (e.g., email format, password complexity)
    # Example:
    # if len(password) < 8:
    #     return jsonify({"error": "Password must be at least 8 characters long"}), 400

    # 3. Check if username or email already exists
    existing_user_by_username = User.query.filter_by(username=username).first()
    if existing_user_by_username:
        return jsonify({"error": f"Username '{username}' already exists"}), 409 # 409 Conflict

    existing_user_by_email = User.query.filter_by(email=email).first()
    if existing_user_by_email:
        return jsonify({"error": f"Email '{email}' already registered"}), 409 # 409 Conflict

    # 4. Create new User instance (hashing happens in User model's __init__)
    try:
        new_user = User(username=username, email=email, password=password)

        # 5. Add new user to the database session
        db.session.add(new_user)

        # 6. Commit the transaction
        db.session.commit()

        # 7. Return success response
        # It's good practice to return the created resource (or its ID/relevant info)
        # Avoid returning the password hash
        return jsonify({
            "message": "User registered successfully",
            "user": {
                "id": new_user.id,
                "username": new_user.username,
                "email": new_user.email,
                "created_at": new_user.created_at.isoformat() + 'Z' # ISO 8601 format
            }
        }), 201 # 201 Created

    except IntegrityError as e:
        # This handles potential race conditions if two requests try to register
        # the same username/email simultaneously, even after the initial check.
        db.session.rollback() # Rollback the session in case of error
        # Log the error for debugging
        print(f"Database Integrity Error during registration: {e}")
        return jsonify({"error": "Database error: Could not register user due to conflicting data."}), 500
    except Exception as e:
        # Catch other potential errors during user creation or commit
        db.session.rollback()
        # Log the generic error
        print(f"Unexpected Error during registration: {e}")
        return jsonify({"error": "An unexpected error occurred during registration."}), 500


@auth_bp.route('/login', methods=['POST'])
def login():
    """Handles user login and issues JWT tokens."""
    # 1. Get data from the incoming JSON request
    data = request.get_json()
    if not data:
        return jsonify({"error": "Request body must be JSON"}), 400

    email = data.get('email')
    password = data.get('password')

    # 2. Basic Input Validation
    if not email or not password:
        return jsonify({"error": "Missing required fields (email, password)"}), 400

    # 3. Find the user by email
    user = User.query.filter_by(email=email).first()

    # 4. Check if user exists and password is correct
    # Uses the check_password method defined in the User model
    if user and user.check_password(password):
        # 5. Credentials are valid, create JWT tokens
        # The 'identity' is the data stored within the JWT payload.
        # It's common to use the user's ID as the identity.
        access_token = create_access_token(identity=user.id, fresh=True) # 'fresh' indicates login just happened
        refresh_token = create_refresh_token(identity=user.id)

        # 6. Return the tokens
        return jsonify(
            access_token=access_token,
            refresh_token=refresh_token
        ), 200
    else:
        # 7. Invalid credentials
        return jsonify({"error": "Invalid email or password"}), 401 # 401 Unauthorized


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

