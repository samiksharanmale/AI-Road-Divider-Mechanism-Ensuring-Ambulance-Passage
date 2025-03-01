from datetime import datetime

class Notification:
    def __init__(self, id, message, created_at=None):
        """
        Initialize a Notification instance.

        Args:
        - id (int): Unique identifier for the notification.
        - message (str): The notification message.
        - created_at (datetime, optional): Timestamp for when the notification was created.
        """
        self.id = id
        self.message = message
        self.created_at = created_at or datetime.now()

    def to_dict(self):
        """
        Convert the notification instance to a dictionary.

        Returns:
        - dict: A dictionary representation of the notification.
        """
        return {
            "id": self.id,
            "message": self.message,
            "created_at": self.created_at.strftime("%Y-%m-%d %H:%M:%S")
        }

class NotificationManager:
    def __init__(self):
        """
        Initialize the NotificationManager with an empty list of notifications.
        """
        self.notifications = []

    def add_notification(self, message):
        """
        Add a new notification to the list.

        Args:
        - message (str): The notification message.
        """
        notification_id = len(self.notifications) + 1
        notification = Notification(id=notification_id, message=message)
        self.notifications.append(notification)

    def get_notifications(self, limit=10):
        """
        Retrieve the latest notifications.

        Args:
        - limit (int): The number of notifications to retrieve.

        Returns:
        - list: A list of the latest notifications as dictionaries.
        """
        return [notification.to_dict() for notification in self.notifications[-limit:]]

# Example usage:
if __name__ == "__main__":
    manager = NotificationManager()
    manager.add_notification("Ambulance detected on Lane 2.")
    manager.add_notification("Traffic cleared for Ambulance ID: A123.")
    print(manager.get_notifications())
