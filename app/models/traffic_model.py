from datetime import datetime
import heapq
import random

class TrafficData:
    def __init__(self, lane_id, congestion_level, vehicles=None, ambulance_detected=False, timestamp=None):
        """
        Initializes traffic data for a specific lane.

        Parameters:
        - lane_id (int): Identifier for the lane.
        - congestion_level (str): Congestion level (e.g., "Clear", "Moderate", "Heavy").
        - vehicles (int, optional): Number of vehicles detected in the lane.
        - ambulance_detected (bool): Whether an ambulance is detected in the lane.
        - timestamp (datetime, optional): Time of the traffic data recording. Defaults to current time.
        """
        self.lane_id = lane_id
        self.congestion_level = congestion_level
        self.vehicles = vehicles or random.randint(5, 50)  # Simulated vehicle count
        self.ambulance_detected = ambulance_detected
        self.timestamp = timestamp or datetime.now()

    def __str__(self):
        """
        String representation of the traffic data.
        """
        ambulance_status = "Ambulance Detected" if self.ambulance_detected else "No Ambulance"
        return f"Lane {self.lane_id} | Congestion: {self.congestion_level} | Vehicles: {self.vehicles} | {ambulance_status} | Timestamp: {self.timestamp}"


class TrafficManager:
    def __init__(self):
        """
        Initializes the traffic manager to store traffic data for all lanes and manage route calculations.
        """
        self.traffic_records = []
        self.road_graph = {}  # Graph representation for shortest path calculation

    def update_traffic_data(self, lane_id, congestion_level, vehicles=None, ambulance_detected=False):
        """
        Updates traffic data for a specific lane.

        Parameters:
        - lane_id (int): Identifier for the lane.
        - congestion_level (str): Congestion level (e.g., "Clear", "Moderate", "Heavy").
        - vehicles (int, optional): Number of vehicles detected in the lane.
        - ambulance_detected (bool): Whether an ambulance is detected in the lane.
        """
        traffic_data = TrafficData(lane_id, congestion_level, vehicles, ambulance_detected)
        self.traffic_records.append(traffic_data)
        print(f"Updated Traffic Data: {traffic_data}")

    def get_latest_traffic_data(self):
        """
        Retrieves the most recent traffic data for each lane.

        Returns:
        - dict: Latest traffic data grouped by lane.
        """
        latest_data = {}
        for record in self.traffic_records:
            if record.lane_id not in latest_data or record.timestamp > latest_data[record.lane_id].timestamp:
                latest_data[record.lane_id] = record
        return latest_data

    def get_all_traffic_records(self):
        """
        Retrieves all traffic data records.

        Returns:
        - list: List of TrafficData objects.
        """
        return self.traffic_records

    def update_road_graph(self, road_connections):
        """
        Updates the graph representation of roads.

        Parameters:
        - road_connections (dict): Dictionary where keys are lanes, and values are lists of (neighboring_lane, weight).
        """
        self.road_graph = road_connections

    def calculate_shortest_path(self, start_lane, destination_lane):
        """
        Implements Dijkstra's algorithm to calculate the shortest path between two lanes.

        Parameters:
        - start_lane (int): The starting lane ID.
        - destination_lane (int): The target lane ID.

        Returns:
        - list: The shortest path as a list of lane IDs.
        - int: The total travel time.
        """
        if start_lane not in self.road_graph or destination_lane not in self.road_graph:
            return [], float('inf')

        pq = [(0, start_lane)]  # Priority queue (travel_time, lane)
        shortest_times = {lane: float('inf') for lane in self.road_graph}
        shortest_times[start_lane] = 0
        previous_nodes = {}

        while pq:
            current_time, current_lane = heapq.heappop(pq)

            if current_lane == destination_lane:
                break

            for neighbor, travel_time in self.road_graph[current_lane]:
                time = current_time + travel_time
                if time < shortest_times[neighbor]:
                    shortest_times[neighbor] = time
                    previous_nodes[neighbor] = current_lane
                    heapq.heappush(pq, (time, neighbor))

        # Reconstruct path
        path = []
        lane = destination_lane
        while lane in previous_nodes:
            path.append(lane)
            lane = previous_nodes[lane]
        path.append(start_lane)
        path.reverse()

        return path, shortest_times[destination_lane]

    def simulate_random_traffic_change(self):
        """
        Randomly alters the congestion levels of some lanes to simulate real-time changes.
        """
        congestion_levels = ["Clear", "Moderate", "Heavy"]
        for record in self.traffic_records:
            new_congestion = random.choice(congestion_levels)
            record.congestion_level = new_congestion
            record.vehicles = random.randint(5, 50)
        print("Traffic conditions updated randomly.")

    def assign_hospital(self, location, hospital_list):
        """
        Returns a dropdown of hospitals based on the location.

        Parameters:
        - location (str): The selected location (e.g., "Pune").
        - hospital_list (dict): Dictionary of locations and their hospitals.

        Returns:
        - list: List of hospitals in the selected location.
        """
        return hospital_list.get(location, ["No hospitals found"])

# Example Usage
if __name__ == "__main__":
    traffic_manager = TrafficManager()
    
    # Simulating traffic updates
    traffic_manager.update_traffic_data(1, "Moderate")
    traffic_manager.update_traffic_data(2, "Clear", ambulance_detected=True)
    traffic_manager.update_traffic_data(3, "Heavy")

    print("Latest Traffic Data:")
    for lane_id, data in traffic_manager.get_latest_traffic_data().items():
        print(data)

    print("\nAll Traffic Records:")
    for record in traffic_manager.get_all_traffic_records():
        print(record)

    # Example road graph and shortest path calculation
    road_connections = {
        1: [(2, 5), (3, 10)],
        2: [(1, 5), (3, 2)],
        3: [(1, 10), (2, 2)]
    }

    traffic_manager.update_road_graph(road_connections)
    shortest_path, travel_time = traffic_manager.calculate_shortest_path(1, 3)
    print(f"\nShortest Path from Lane 1 to Lane 3: {shortest_path} (Time: {travel_time} min)")

    # Simulate random traffic condition changes
    traffic_manager.simulate_random_traffic_change()

    # Hospital selection based on location
    hospitals = {
        "Pune": ["Apollo Hospital", "Sahyadri Hospital", "Ruby Hall Clinic"],
        "Mumbai": ["Tata Memorial", "Hiranandani Hospital", "Lilavati Hospital"]
    }
    selected_hospitals = traffic_manager.assign_hospital("Pune", hospitals)
    print(f"\nHospitals in Pune: {selected_hospitals}")
