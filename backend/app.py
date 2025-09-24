from flask import Flask
from flask_cors import CORS
from routes.vehicle_routes import vehicle_bp
from routes.analytics_routes import analytics_bp
from models.data import load_vehicles, load_customers

app = Flask(__name__)
CORS(app)

## Register blueprints
app.register_blueprint(vehicle_bp)
app.register_blueprint(analytics_bp)

if __name__ == "__main__":
    load_vehicles()
    load_customers()
    app.run(debug=True)
