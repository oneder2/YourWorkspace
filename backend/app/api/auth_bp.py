# /your_project_root/app/api/auth_bp.py
# Blueprint for authentication-related API endpoints.

from flask import Blueprint, jsonify, request
from sqlalchemy.exc import IntegrityError
import datetime # For blocklist entry creation and timezone

# Import database session, models, and bcrypt instance
from ..extensions import db, bcrypt, jwt # Import jwt from extensions
from ..models.user import User
from ..models.token_blocklist import TokenBlocklist # Import TokenBlocklist model

# Import JWT functions
from flask_jwt_extended import (
    create_access_token,
    create_refresh_token,
    jwt_required,
    get_jwt_identity,
    get_jwt # To access full JWT data (like jti, type)
)

auth_bp = Blueprint('auth', __name__)

# --- JWT Callback for Blocklisting ---
@jwt.token_in_blocklist_loader
def check_if_token_is_revoked(jwt_header, jwt_payload: dict):
    """
    Callback function to check if a JWT has been revoked (blocklisted).
    """
    jti = jwt_payload['jti']
    token = TokenBlocklist.query.filter_by(jti=jti).one_or_none()
    return token is not None


# --- API Endpoints ---
@auth_bp.route('/ping', methods=['GET'])
def ping_auth():
    """Simple test route."""
    return jsonify({"message": "Auth API is alive!"}), 200


@auth_bp.route('/register', methods=['POST'])
def register():
    """Handles user registration."""
    data = request.get_json()
    if not data:
        return jsonify({"error": "Request body must be JSON"}), 400

    username = data.get('username')
    email = data.get('email')
    password = data.get('password')

    if not username or not email or not password:
        return jsonify({"error": "Missing required fields (username, email, password)"}), 400

    if User.query.filter_by(username=username).first(): # Still okay for checking existence
        return jsonify({"error": f"Username '{username}' already exists"}), 409

    if User.query.filter_by(email=email).first(): # Still okay for checking existence
        return jsonify({"error": f"Email '{email}' already registered"}), 409

    try:
        new_user = User(username=username, email=email, password=password)
        db.session.add(new_user)
        db.session.commit()
        return jsonify({
            "message": "User registered successfully",
            "user": {
                "id": new_user.id,
                "username": new_user.username,
                "email": new_user.email,
                "created_at": new_user.created_at.isoformat() + 'Z' # Assuming created_at is UTC
            }
        }), 201
    except IntegrityError as e:
        db.session.rollback()
        print(f"Database Integrity Error during registration: {e}")
        return jsonify({"error": "Database error: Could not register user."}), 500
    except Exception as e:
        db.session.rollback()
        print(f"Unexpected Error during registration: {e}")
        return jsonify({"error": "An unexpected error occurred."}), 500


@auth_bp.route('/login', methods=['POST'])
def login():
    """Handles user login and issues JWT tokens."""
    data = request.get_json()
    if not data:
        return jsonify({"error": "Request body must be JSON"}), 400

    email = data.get('email')
    password = data.get('password')

    if not email or not password:
        return jsonify({"error": "Missing required fields (email, password)"}), 400

    user = User.query.filter_by(email=email).first() # Okay for login check

    if user and user.check_password(password):
        user_identity = str(user.id)
        access_token = create_access_token(identity=user_identity, fresh=True)
        refresh_token = create_refresh_token(identity=user_identity)
        return jsonify(
            access_token=access_token,
            refresh_token=refresh_token
        ), 200
    else:
        return jsonify({"error": "Invalid email or password"}), 401


@auth_bp.route('/logout', methods=['POST'])
@jwt_required()
def logout():
    """Revokes the current user's access token."""
    token_payload = get_jwt()
    jti = token_payload['jti']
    token_type = token_payload['type']
    current_user_id_str = get_jwt_identity()

    try:
        blocklisted_token = TokenBlocklist(
            jti=jti,
            token_type=token_type,
            user_id=int(current_user_id_str),
            # Use timezone-aware UTC datetime
            created_at=datetime.datetime.now(datetime.timezone.utc)
        )
        db.session.add(blocklisted_token)
        db.session.commit()
        return jsonify({"message": "Access token revoked. User logged out."}), 200
    except Exception as e:
        db.session.rollback()
        print(f"Error blocklisting token: {e}")
        return jsonify({"error": "Could not process logout request."}), 500


@auth_bp.route('/logout-refresh', methods=['POST'])
@jwt_required(refresh=True)
def logout_refresh():
    """Revokes the current user's refresh token."""
    token_payload = get_jwt()
    jti = token_payload['jti']
    token_type = token_payload['type']
    current_user_id_str = get_jwt_identity()

    try:
        blocklisted_token = TokenBlocklist(
            jti=jti,
            token_type=token_type,
            user_id=int(current_user_id_str),
            # Use timezone-aware UTC datetime
            created_at=datetime.datetime.now(datetime.timezone.utc)
        )
        db.session.add(blocklisted_token)
        db.session.commit()
        return jsonify({"message": "Refresh token revoked."}), 200
    except Exception as e:
        db.session.rollback()
        print(f"Error blocklisting refresh token: {e}")
        return jsonify({"error": "Could not process logout request for refresh token."}), 500


@auth_bp.route('/me', methods=['GET'])
@jwt_required()
def get_current_user_profile():
    """Gets the profile of the currently authenticated user."""
    current_user_id_str = get_jwt_identity()
    try:
        # Use db.session.get() for SQLAlchemy 2.0 compatibility
        user = db.session.get(User, int(current_user_id_str))
    except ValueError:
        return jsonify({"error": "Invalid user identity format"}), 400

    if not user:
        return jsonify({"error": "User not found"}), 404

    return jsonify({
        "id": user.id,
        "username": user.username,
        "email": user.email,
        # Assuming these are stored as UTC and you want to represent them as such
        "created_at": user.created_at.isoformat() + 'Z',
        "updated_at": user.updated_at.isoformat() + 'Z'
    }), 200


@auth_bp.route('/refresh', methods=['POST'])
@jwt_required(refresh=True)
def refresh_access_token():
    """Gets a new access token using a refresh token."""
    current_user_id_str = get_jwt_identity()
    new_access_token = create_access_token(identity=current_user_id_str, fresh=False)
    return jsonify(access_token=new_access_token), 200


@auth_bp.route('/change-password', methods=['POST'])
@jwt_required(fresh=True)
def change_password():
    """Changes the current user's password (requires a fresh token)."""
    current_user_id_str = get_jwt_identity()
    data = request.get_json()
    new_password = data.get('new_password')

    if not new_password:
        return jsonify({"error": "New password is required"}), 400
    
    try:
        # Use db.session.get() for SQLAlchemy 2.0 compatibility
        user = db.session.get(User, int(current_user_id_str))
    except ValueError:
        return jsonify({"error": "Invalid user identity format"}), 400

    if not user:
        return jsonify({"error": "User not found"}), 404

    try:
        user.set_password(new_password)
        db.session.commit()
        return jsonify({"message": "Password updated successfully."}), 200
    except Exception as e:
        db.session.rollback()
        print(f"Error changing password: {e}")
        return jsonify({"error": "Could not update password."}), 500
