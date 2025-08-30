from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from backend.app.services.auth_service import AuthService

auth_bp = Blueprint('auth_bp', __name__)

@auth_bp.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    username = data.get('username')
    email = data.get('email')
    password = data.get('password')

    if not all([username, email, password]):
        return jsonify({"msg": "Missing username, email, or password"}), 400

    user = AuthService.register_user(username, email, password)

    if user is None:
        return jsonify({"msg": "User with that username or email already exists"}), 409

    return jsonify({"msg": "User created successfully"}), 201


@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')

    if not all([username, password]):
        return jsonify({"msg": "Missing username or password"}), 400

    user = AuthService.authenticate_user(username, password)

    if user is None:
        return jsonify({"msg": "Bad username or password"}), 401

    # Identity can be the user ID or any other unique identifier
    access_token = create_access_token(identity=user.id)
    return jsonify(access_token=access_token)


@auth_bp.route('/profile', methods=['GET'])
@jwt_required()
def profile():
    # Access the identity of the current user with get_jwt_identity
    current_user_id = get_jwt_identity()
    # Here you would typically fetch the user from the database
    # For now, just return the identity
    return jsonify(logged_in_as=current_user_id), 200
