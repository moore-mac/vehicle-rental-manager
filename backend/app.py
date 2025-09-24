from flask import Flask
from flask_cors import CORS
from utils.data_handler import load_vehicles, load_customers

app = Flask(__name__)
CORS(app)

load_vehicles()
load_customers()

from routes.vehicle_routes import vehicle_bp
from routes.analytics_routes import analytics_bp

app.register_blueprint(vehicle_bp)
app.register_blueprint(analytics_bp)

if __name__ == "__main__":
    app.run(debug=True)
