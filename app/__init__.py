from flask import Flask

app = Flask(__name__)
app.config.from_pyfile('config.py')

# Import blueprints
from app.routes.ambulance import ambulance_bp
from app.routes.traffic import traffic_bp
from app.routes.notifications import notifications_bp

# Register blueprints
app.register_blueprint(ambulance_bp, url_prefix='/ambulance')
app.register_blueprint(traffic_bp, url_prefix='/traffic')
app.register_blueprint(notifications_bp, url_prefix='/notifications')
