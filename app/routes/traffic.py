from flask import Blueprint, jsonify, request
from app.models.traffic_model import TrafficManager

traffic_bp = Blueprint('traffic', __name__)
traffic_manager = TrafficManager()

@traffic_bp.route('/traffic', methods=['GET'])
def get_all_traffic_data():
    """
    Endpoint to retrieve all traffic data.
    """
    traffic_data = [
        {
            "lane_id": record.lane_id,
            "congestion_level": record.congestion_level,
            "vehicles": record.vehicles,
            "ambulance_detected": record.ambulance_detected,
            "timestamp": record.timestamp.strftime("%Y-%m-%d %H:%M:%S")
        }
        for record in traffic_manager.get_all_traffic_records()
    ]
    return jsonify(traffic_data), 200

@traffic_bp.route('/traffic/<int:lane_id>', methods=['GET'])
def get_traffic_data_by_lane(lane_id):
    """
    Endpoint to retrieve traffic data for a specific lane.
    """
    latest_data = traffic_manager.get_latest_traffic_data()
    traffic_data = latest_data.get(lane_id)
    
    if traffic_data:
        return jsonify({
            "lane_id": traffic_data.lane_id,
            "congestion_level": traffic_data.congestion_level,
            "vehicles": traffic_data.vehicles,
            "ambulance_detected": traffic_data.ambulance_detected,
            "timestamp": traffic_data.timestamp.strftime("%Y-%m-%d %H:%M:%S")
        }), 200
    
    return jsonify({"error": "Traffic data not found for the specified lane"}), 404

@traffic_bp.route('/traffic/update', methods=['POST'])
def update_traffic_data():
    """
    Endpoint to update traffic data for a lane.
    """
    data = request.get_json()
    if not data or 'lane_id' not in data or 'congestion_level' not in data:
        return jsonify({"error": "Missing required fields (lane_id, congestion_level)"}), 400
    
    traffic_manager.update_traffic_data(
        lane_id=data['lane_id'],
        congestion_level=data['congestion_level'],
        vehicles=data.get('vehicles'),
        ambulance_detected=data.get('ambulance_detected', False)
    )
    
    return jsonify({"message": "Traffic data updated successfully"}), 200

@traffic_bp.route('/traffic/clear', methods=['POST'])
def clear_traffic_for_ambulance():
    """
    Endpoint to clear traffic for an ambulance.
    """
    data = request.get_json()
    if not data or 'lane_id' not in data:
        return jsonify({"error": "Missing required field: lane_id"}), 400
    
    latest_data = traffic_manager.get_latest_traffic_data()
    if data['lane_id'] not in latest_data:
        return jsonify({"error": "Lane ID not found in traffic data"}), 404
    
    traffic_manager.update_traffic_data(
        lane_id=data['lane_id'],
        congestion_level="Clear",
        vehicles=0,
        ambulance_detected=True
    )
    
    return jsonify({"message": "Traffic cleared for the ambulance"}), 200
