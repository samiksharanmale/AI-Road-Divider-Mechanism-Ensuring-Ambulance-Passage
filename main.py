from flask import Flask, render_template, request, redirect, url_for, Response, flash
import cv2
import os

app = Flask(__name__)
app.secret_key = "supersecretkey"  # Required for flashing messages

# Dummy user data for login
users = {"admin": "password"}

# Path to the input video file
VIDEO_PATH = "data/input.mp4"

# Video feed generator
def generate_video_feed():
    # Check if the video file exists
    if not os.path.exists(VIDEO_PATH):
        raise FileNotFoundError(f"Video file not found at {VIDEO_PATH}")

    cap = cv2.VideoCapture(VIDEO_PATH)
    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break
        # Simulate lane detection (replace with real detection logic)
        cv2.line(frame, (100, 500), (400, 300), (255, 0, 0), 10)
        _, buffer = cv2.imencode('.jpg', frame)
        frame = buffer.tobytes()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')
    cap.release()

# Routes
@app.route('/')
def index():
    """Render the homepage with options to login or try the system."""
    return render_template('index.html')

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

@app.route('/live_feed')
def live_feed():
    """Stream the live feed with lane detection."""
    try:
        return Response(generate_video_feed(), mimetype='multipart/x-mixed-replace; boundary=frame')
    except FileNotFoundError as e:
        flash(str(e))
        return redirect(url_for('index'))
    
@app.route('/notifications')
def notifications():
    """Render the notifications page."""
    return render_template('notifications.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    """Handle user login."""
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if users.get(username) == password:
            flash(f"Welcome, {username}!")
            return redirect(url_for('index'))
        else:
            flash("Invalid username or password. Please try again.")
            return redirect(url_for('login'))
    return render_template('login.html')

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    """Handle user sign-up."""
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if username in users:
            flash("Username already exists! Please choose a different one.")
            return redirect(url_for('signup'))
        users[username] = password
        flash("Account created successfully! Please login.")
        return redirect(url_for('login'))
    return render_template('signup.html')

if __name__ == "__main__":
    # Ensure the video file exists in the data directory
    if not os.path.exists(VIDEO_PATH):
        print(f"Error: Video file not found at {VIDEO_PATH}")
        print("Please place the video file in the 'data/' directory and restart the app.")
    else:
        app.run(debug=True)
