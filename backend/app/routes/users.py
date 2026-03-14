from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from backend.app.services.user_service import UserService
from backend.app.models.user import User

user_bp = Blueprint('user_bp', __name__)

def serialize_user(user):
    """Helper function to serialize a user object."""
    return {
        'id': user.id,
        'username': user.username,
        'email': user.email,
        'role': user.role,
        'created_at': user.created_at.isoformat(),
        'updated_at': user.updated_at.isoformat()
    }

@user_bp.route('', methods=['GET'])
@jwt_required()
def get_users():
    users = UserService.get_all_users()
    return jsonify([serialize_user(u) for u in users]), 200

@user_bp.route('/<int:user_id>', methods=['GET'])
@jwt_required()
def get_user(user_id):
    user = UserService.get_user_by_id(user_id)
    if not user:
        return jsonify({"msg": "User not found"}), 404
    return jsonify(serialize_user(user)), 200

@user_bp.route('', methods=['POST'])
@jwt_required()
def create_user():
    data = request.get_json()
    user, msg = UserService.create_user(data)

    if user is None:
        return jsonify({"msg": msg}), 400

    return jsonify(serialize_user(user)), 201

@user_bp.route('/<int:user_id>', methods=['PUT'])
@jwt_required()
def update_user(user_id):
    data = request.get_json()
    user, msg = UserService.update_user(user_id, data)

    if user is None:
        return jsonify({"msg": msg}), 404

    return jsonify(serialize_user(user)), 200

@user_bp.route('/<int:user_id>', methods=['DELETE'])
@jwt_required()
def delete_user(user_id):
    success, msg = UserService.delete_user(user_id)

    if not success:
        return jsonify({"msg": msg}), 404

    return jsonify({"msg": msg}), 200
