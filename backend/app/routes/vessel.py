from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from backend.app.services.vessel_service import VesselService
from backend.app.models.vessel import Vessel # For serialization

vessel_bp = Blueprint('vessel_bp', __name__)

def serialize_vessel(vessel):
    """Helper function to serialize a vessel object."""
    return {
        'id': vessel.id,
        'mmsi': vessel.mmsi,
        'name': vessel.name,
        'vessel_type': vessel.vessel_type,
        'length_m': str(vessel.length_m) if vessel.length_m is not None else None,
        'beam_m': str(vessel.beam_m) if vessel.beam_m is not None else None,
        'owner_id': vessel.owner_id,
        'created_at': vessel.created_at.isoformat(),
        'updated_at': vessel.updated_at.isoformat()
    }

@vessel_bp.route('', methods=['GET'])
@jwt_required()
def get_vessels():
    vessels = VesselService.get_all_vessels()
    return jsonify([serialize_vessel(v) for v in vessels]), 200

@vessel_bp.route('/<int:vessel_id>', methods=['GET'])
@jwt_required()
def get_vessel(vessel_id):
    vessel = VesselService.get_vessel_by_id(vessel_id)
    if not vessel:
        return jsonify({"msg": "Vessel not found"}), 404
    return jsonify(serialize_vessel(vessel)), 200

@vessel_bp.route('', methods=['POST'])
@jwt_required()
def create_vessel():
    current_user_id = get_jwt_identity()
    data = request.get_json()

    vessel, msg = VesselService.create_vessel(data, owner_id=current_user_id)

    if vessel is None:
        return jsonify({"msg": msg}), 400

    return jsonify(serialize_vessel(vessel)), 201

@vessel_bp.route('/<int:vessel_id>', methods=['PUT'])
@jwt_required()
def update_vessel(vessel_id):
    data = request.get_json()
    vessel, msg = VesselService.update_vessel(vessel_id, data)

    if vessel is None:
        return jsonify({"msg": msg}), 404

    return jsonify(serialize_vessel(vessel)), 200

@vessel_bp.route('/<int:vessel_id>', methods=['DELETE'])
@jwt_required()
def delete_vessel(vessel_id):
    # In a real app, you'd add more authorization logic here
    # to ensure the user has permission to delete the vessel.
    success, msg = VesselService.delete_vessel(vessel_id)

    if not success:
        return jsonify({"msg": msg}), 404

    return jsonify({"msg": msg}), 200
