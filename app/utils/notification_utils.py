import datetime
import json
import os

# Path for storing notification logs
LOG_FILE = "notifications.log"

def log_notification(message, notification_type="INFO"):
    """
    Log a notification to the log file with a timestamp.
    
    Args:
        message (str): The notification message to log.
        notification_type (str): The type of notification (INFO, WARNING, ERROR).
    """
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    log_entry = {
        "timestamp": timestamp,
        "type": notification_type,
        "message": message
    }

    # Append the log entry to the log file
    with open(LOG_FILE, "a") as log_file:
        log_file.write(json.dumps(log_entry) + "\n")

    print(f"[{timestamp}] [{notification_type}] {message}")


def get_recent_notifications(limit=5):
    """
    Retrieve the most recent notifications from the log file.
    
    Args:
        limit (int): Number of recent notifications to retrieve.
        
    Returns:
        list: A list of recent notification messages.
    """
    if not os.path.exists(LOG_FILE):
        return ["No notifications available."]

    with open(LOG_FILE, "r") as log_file:
        lines = log_file.readlines()

    # Return the most recent notifications (up to the limit)
    recent_logs = [json.loads(line.strip()) for line in lines[-limit:]]
    return recent_logs


def simulate_notification_sending():
    """
    Simulate sending notifications to demonstrate the functionality.
    This can be replaced with actual logic for sending notifications.
    """
    sample_notifications = [
        "Ambulance approaching Lane 2.",
        "Heavy traffic detected on Lane 3.",
        "Clear path created for emergency vehicle.",
        "Lane priority shifted to Lane 4.",
        "Intersection ahead cleared for ambulance.",
    ]

    for message in sample_notifications:
        log_notification(message)


def clear_notifications():
    """
    Clear all notifications from the log file.
    """
    if os.path.exists(LOG_FILE):
        open(LOG_FILE, "w").close()
        print("All notifications have been cleared.")
    else:
        print("No notifications to clear.")


if __name__ == "__main__":
    # Example: Simulate notifications and display recent ones
    simulate_notification_sending()

    print("\nRecent Notifications:")
    recent = get_recent_notifications()
    for entry in recent:
        print(f"[{entry['timestamp']}] [{entry['type']}] {entry['message']}")
