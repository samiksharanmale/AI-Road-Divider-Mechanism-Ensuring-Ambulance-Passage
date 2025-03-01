from flask import Flask, render_template, request, redirect, url_for, Response, flash, session, g
import cv2
import os
import random
import googlemaps
import time
import bcrypt
import csv

app = Flask(__name__)
app.secret_key = "AIzaSyD5liXKSRtFhif83lbqxoJYeS-vb1gqtSo222"  # Required for flashing messages

USER_CSV_FILE = "users.csv"

# List of videos to choose from
VIDEO_FILES = ["data/output1.mp4", "data/output2.mp4"]

# Initialize Google Maps API
gmaps = googlemaps.Client(key='AIzaSyD5liXKSRtFhif83lbqxoJYeS-vb1gqtSo')

if not os.path.exists(USER_CSV_FILE):
    with open(USER_CSV_FILE, mode="w", newline="") as file:
        writer = csv.writer(file)
        writer.writerow(["id", "username", "password"])

def generate_video_feed():
    """Randomly select a video and generate lane-detected frames."""
    video_path = random.choice(VIDEO_FILES)
    
    if not os.path.exists(video_path):
        raise FileNotFoundError(f"Video file not found at {video_path}")

    cap = cv2.VideoCapture(video_path)

    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break

        # Apply simulated lane detection (replace this with actual logic if needed)
        frame = simulate_lane_detection(frame)

        # Encode the frame as JPEG for streaming
        _, buffer = cv2.imencode('.jpg', frame)
        frame = buffer.tobytes()
        
        time.sleep(0.05)

        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')
    
    cap.release()

def simulate_lane_detection(frame):
    """
    Simulate lane detection by drawing example lane lines.
    Replace this function with actual lane detection logic if needed.
    """
    height, width = frame.shape[:2]

    # Example lane markers (can be replaced by real lane detection)
    cv2.line(frame, (int(width * 0.3), height), (int(width * 0.45), int(height * 0.5)), (0, 255, 0), 10)
    cv2.line(frame, (int(width * 0.7), height), (int(width * 0.55), int(height * 0.5)), (0, 255, 0), 10)

    # Optional: Add text overlay for debugging
    cv2.putText(frame, "Lane Detection Active", (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

    return frame

# Routes
@app.route('/')
def index():
    """Render the homepage with options to login or try the system."""
    return render_template('index.html')

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    """User signup functionality using CSV file."""
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

        # Read existing users to check if username already exists
        existing_users = []
        with open(USER_CSV_FILE, mode="r") as file:
            reader = csv.reader(file)
            next(reader)  # Skip header
            for row in reader:
                existing_users.append(row[1])  # Username is in the second column

        if username in existing_users:
            flash("Username already exists. Please choose another.", "danger")
        else:
            # Get new user ID (increment from last user ID)
            new_id = len(existing_users) + 1
            with open(USER_CSV_FILE, mode="a", newline="") as file:
                writer = csv.writer(file)
                writer.writerow([new_id, username, hashed_password])
            flash("Signup successful! Please log in.", "success")
            return redirect(url_for('login'))

    return render_template('signup.html')

@app.route('/driver-login', methods=['GET', 'POST'])
def driver_login():
    if request.method == 'POST':
        phone = request.form['phone']
        password = request.form['password'].encode('utf-8')
        
        # Read drivers.csv and check credentials
        try:
            with open("drivers.csv", "r") as file:
                reader = csv.reader(file)
                for row in reader:
                    stored_phone, stored_password = row
                    if phone == stored_phone and bcrypt.checkpw(password, stored_password.encode('utf-8')):
                        flash("Login successful!", "success")
                        return redirect(url_for('driver_dashboard'))  # Redirect to driver dashboard
        except FileNotFoundError:
            flash("No registered drivers found.", "danger")
        
        flash("Invalid phone number or password!", "danger")

    return render_template('driver_login.html')


@app.route('/driver-signup', methods=['GET', 'POST'])
def driver_signup():
    if request.method == 'POST':
        phone = request.form['phone']
        password = bcrypt.hashpw(request.form['password'].encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

        # Store new driver credentials in drivers.csv
        with open("drivers.csv", "a", newline="") as file:
            writer = csv.writer(file)
            writer.writerow([phone, password])
        
        flash("Signup successful! Please log in.", "success")
        return redirect(url_for('driver_login'))

    return render_template('driver_signup.html')


@app.route("/driver-authenticate", methods=["POST"])
def driver_authenticate():
    phone = request.form.get("phone")
    password = request.form.get("password")

    if phone in DRIVER_CREDENTIALS and DRIVER_CREDENTIALS[phone] == password:
        session["driver_logged_in"] = True
        return redirect(url_for("driver_dashboard"))
    else:
        return render_template("driver-login.html", error="Invalid phone number or password")

@app.route('/driver_dashboard')
def driver_dashboard():
    if 'driver_id' not in session:
        flash("Please log in as a driver to view requests.")
        return redirect(url_for('driver_login'))

    requests = []
    with open("ambulance_requests.csv", "r") as file:
        reader = csv.reader(file)
        for row in reader:
            requests.append(row)  # Store each request

    return render_template('driver_dashboard.html', requests=requests)


@app.route('/request_ambulance', methods=['POST'])
def request_ambulance():
    if 'user_id' not in session:
        flash("Please log in to request an ambulance.")
        return redirect(url_for('login'))

    start_location = request.form.get('start_location')
    end_location = request.form.get('end_location')

    if not start_location or not end_location:
        flash("Please fill in both start and end locations.")
        return redirect(url_for('ambulance_details'))

    user_id = session['user_id']

    # Save request in CSV
    with open("ambulance_requests.csv", "a", newline="") as file:
        writer = csv.writer(file)
        writer.writerow([user_id, start_location, end_location, "pending"])

    flash("Request sent to drivers successfully!")
    return redirect(url_for('traffic_simulation'))

@app.route('/send_message', methods=['POST'])
def send_message():
    if 'user_id' not in session:
        flash("Please log in to send a message.")
        return redirect(url_for('login'))

    user_id = session['user_id']
    message = request.form['message']

    # Store message in CSV file
    with open("messages.csv", "a") as file:
        file.write(f"{user_id},{message}\n")

    flash("Emergency message sent successfully!")
    return redirect(url_for('profile'))


@app.route('/accept_request', methods=['POST'])
def accept_request():
    if 'driver_id' not in session:
        flash("Please log in as a driver.")
        return redirect(url_for('driver_login'))

    user_id = request.form['user_id']
    
    # Update CSV to mark request as "accepted"
    rows = []
    with open("ambulance_requests.csv", "r") as file:
        reader = csv.reader(file)
        for row in reader:
            if row[0] == user_id:
                row[3] = "accepted"  # Change status to accepted
            rows.append(row)

    with open("ambulance_requests.csv", "w", newline="") as file:
        writer = csv.writer(file)
        writer.writerows(rows)

    flash("Request accepted! You can now start the live feed.")
    return redirect(url_for('driver_dashboard'))


@app.route('/profile')
def profile():
    user_id = session.get('user_id')
    requests = []
    
    with open("ambulance_requests.csv", "r") as file:
        for line in file:
            rid, time = line.strip().split(',')
            if rid == str(user_id):
                requests.append({"id": rid, "time": time})

    return render_template("profile.html", user_requests=requests)


@app.route('/user_logout')
def user_logout():
    if 'user_id' in session:
        session.pop('user_id', None)
        flash("User logged out successfully.")
    return redirect(url_for('login'))

@app.route('/driver_logout')
def driver_logout():
    if 'driver_id' in session:
        session.pop('driver_id', None)
        flash("Driver logged out successfully.")
    return redirect(url_for('driver_login'))


@app.route('/try_now')
def try_now():
    """Render the 'Try Now' page for ambulance info input."""
    return render_template('try_now.html')

@app.route('/fetching', methods=['POST'])
def fetching():
    """Process ambulance input and simulate fetching footage."""
    ambulance_info = request.form.to_dict()
    print("Ambulance Information:", ambulance_info)  # Debugging info
    if not ambulance_info.get("location") or not ambulance_info.get("ambulance_id"):
        flash("Please provide all required information!")
        return redirect(url_for('try_now'))
    return render_template('fetching.html')

@app.route('/ambulance_results', methods=['GET'])
def ambulance_results():
    """Fetch and display available ambulances in the requested location."""
    location = request.args.get('location', 'Nashik')
    ambulances = [
        {"id": "AMB-101", "location": "Nashik City Hospital, MG Road"},
        {"id": "AMB-102", "location": "Nashik General Hospital, Panchavati"},
        {"id": "AMB-103", "location": "Suyash Hospital, Gangapur Road"},
        {"id": "AMB-104", "location": "Wockhardt Hospital, Canada Corner"}
    ]
    return render_template('ambulance_results.html', location=location, ambulances=ambulances)

@app.route('/ambulance_details')
def ambulance_details():
    """Render the form to enter destination and upload video."""
    ambulance_id = request.args.get('ambulance_id')
    return render_template('ambulance_details.html', ambulance_id=ambulance_id)

@app.route('/submit_details', methods=['POST'])
def submit_details():
    """Process the submitted destination and optional video."""
    ambulance_id = request.form['ambulance_id']
    destination = request.form['destination']
    video = request.files['video']

    if video:
        video_path = f"uploaded_videos/{video.filename}"
        os.makedirs("uploaded_videos", exist_ok=True)
        video.save(video_path)
        flash(f"Video uploaded successfully: {video.filename}")

    flash(f"Details for ambulance {ambulance_id} submitted successfully to destination {destination}.")
    return redirect(url_for('ambulance_results'))

@app.route('/live_feed')
def live_feed():
    if 'driver_id' not in session:
        flash("Access denied! Drivers only.")
        return redirect(url_for('driver_login'))
    return render_template('live_feed.html')  

@app.route('/simulate_traffic', methods=['POST'])
def simulate_traffic():
    """Simulate traffic flow between start location and destination."""
    try:
        start_location = request.form['start_location'].strip()
        destination = request.form['destination'].strip()

        if not start_location or not destination:
            flash("Start location and destination cannot be empty.")
            return redirect(url_for('ambulance_details'))

        geocode_start = gmaps.geocode(start_location)
        geocode_destination = gmaps.geocode(destination)

        if not geocode_start or not geocode_destination:
            flash("Invalid locations. Please provide valid addresses.")
            return redirect(url_for('ambulance_details'))

        start_location = geocode_start[0]['formatted_address']
        destination = geocode_destination[0]['formatted_address']

        directions_result = gmaps.directions(start_location, destination)

        if not directions_result:
            flash("Unable to find a route. Please check the locations and try again.")
            return redirect(url_for('ambulance_details'))

        route = directions_result[0]['legs'][0]
        start_address = route['start_address']
        end_address = route['end_address']
        distance = route['distance']['text']
        duration = route['duration']['text']

        return render_template('traffic_simulation.html', 
                               start_location=start_address, 
                               destination=end_address, 
                               distance=distance, 
                               duration=duration)
    except Exception as e:
        flash(f"An error occurred: {str(e)}")
        return redirect(url_for('ambulance_details'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    """User login functionality using CSV file."""
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        with open(USER_CSV_FILE, mode="r") as file:
            reader = csv.reader(file)
            next(reader)  # Skip header
            for row in reader:
                stored_username, stored_password = row[1], row[2]
                if username == stored_username and bcrypt.checkpw(password.encode('utf-8'), stored_password.encode('utf-8')):
                    session['user_id'] = row[0]  # Store user ID in session
                    session['user_name'] = username
                    flash(f"Welcome, {username}!", "success")
                    return redirect(url_for('index'))

        flash("Invalid username or password.", "danger")

    return render_template('login.html')

if __name__ == "__main__":
    app.run(debug=True)
