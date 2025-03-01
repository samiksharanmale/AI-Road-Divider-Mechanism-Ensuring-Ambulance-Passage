from flask import Blueprint, jsonify, request
from app.models.notifications_model import NotificationManager

notifications_bp = Blueprint('notifications', __name__)
notification_manager = NotificationManager()

@notifications_bp.route('/notifications', methods=['GET'])
def get_notifications():
    """
    Endpoint to retrieve all notifications.
    """
    notifications = notification_manager.get_all_notifications()
    return jsonify(notifications), 200

@notifications_bp.route('/notifications/<notification_id>', methods=['GET'])
def get_notification(notification_id):
    """
    Endpoint to retrieve a specific notification by ID.
    """
    notification = notification_manager.get_notification(notification_id)
    if notification:
        return jsonify(notification), 200
    return jsonify({"error": "Notification not found"}), 404

@notifications_bp.route('/notifications', methods=['POST'])
def create_notification():
    """
    Endpoint to create a new notification.
    """
    data = request.get_json()
    if not data or 'message' not in data:
        return jsonify({"error": "Missing required fields"}), 400

    notification_id = notification_manager.create_notification(data['message'])
    return jsonify({"message": "Notification created", "id": notification_id}), 201

@notifications_bp.route('/notifications/<notification_id>', methods=['DELETE'])
def delete_notification(notification_id):
    """
    Endpoint to delete a specific notification by ID.
    """
    deleted = notification_manager.delete_notification(notification_id)
    if deleted:
        return jsonify({"message": "Notification deleted successfully"}), 200
    return jsonify({"error": "Notification not found"}), 404
