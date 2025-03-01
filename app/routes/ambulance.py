from flask import Blueprint, request, jsonify
from app.models.ambulance_model import AmbulanceManager

ambulance_bp = Blueprint('ambulance', __name__)
ambulance_manager = AmbulanceManager()

@ambulance_bp.route('/ambulance/register', methods=['POST'])
def register_ambulance():
    """
    Endpoint to register a new ambulance.
    """
    data = request.get_json()
    if not data or 'ambulance_id' not in data or 'current_location' not in data:
        return jsonify({"error": "Missing required fields"}), 400
    
    ambulance_manager.register_ambulance(data['ambulance_id'], data['current_location'])
    return jsonify({"message": "Ambulance registered successfully"}), 201

@ambulance_bp.route('/ambulance/<ambulance_id>', methods=['GET'])
def get_ambulance_info(ambulance_id):
    """
    Endpoint to retrieve ambulance information.
    """
    ambulance = ambulance_manager.get_ambulance_info(ambulance_id)
    if ambulance:
        return jsonify(ambulance), 200
    return jsonify({"error": "Ambulance not found"}), 404

@ambulance_bp.route('/ambulance/<ambulance_id>/update', methods=['PUT'])
def update_ambulance_location(ambulance_id):
    """
    Endpoint to update the location of an ambulance.
    """
    data = request.get_json()
    if not data or 'current_location' not in data:
        return jsonify({"error": "Missing required fields"}), 400

    updated = ambulance_manager.update_location(ambulance_id, data['current_location'])
    if updated:
        return jsonify({"message": "Location updated successfully"}), 200
    return jsonify({"error": "Ambulance not found"}), 404

@ambulance_bp.route('/ambulances', methods=['GET'])
def get_all_ambulances():
    """
    Endpoint to retrieve all ambulances.
    """
    ambulances = ambulance_manager.get_all_ambulances()
    return jsonify(ambulances), 200
