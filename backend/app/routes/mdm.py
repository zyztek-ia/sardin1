from flask import Blueprint, jsonify, request
from ..services.mdm_service import MDMService

mdm_bp = Blueprint('mdm', __name__)
mdm_service = MDMService()

@mdm_bp.route('/diagnose', methods=['GET'])
def diagnose():
    return jsonify(mdm_service.diagnose_device()), 200

@mdm_bp.route('/unlock', methods=['POST'])
def unlock():
    package = request.json.get('package')
    return jsonify(mdm_service.remove_package(package)), 200

@mdm_bp.route('/ai-fix', methods=['POST'])
def ai_fix():
    data = request.json
    return jsonify({"results": mdm_service.ai_assisted_unlock(data.get('device_info'), data.get('last_error'))}), 200
