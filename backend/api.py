from flask import Flask, jsonify, request
import csv

app = Flask(__name__)

def load_vehicles():
    global vehicles
    with open('backend/vehicle.csv', 'r') as f:
        reader = csv.DictReader(f)
        vehicles = list(reader)

def save_vehicles():
    with open('backend/vehicle.csv', 'w', newline='') as f:
        if vehicles:
            writer = csv.DictWriter(f, fieldnames=vehicles[0].keys())
            writer.writeheader()
            writer.writerows(vehicles)

## Show details of specific vehicle by car reg 
## curl "http://localhost:5000/cars/show?reg=AW69DVJ"
@app.route("/cars/show", methods=["GET"])
def get_reg():
    vehicle_reg = request.args.get("reg")
    for v in vehicles:
        if v["vrm"] == vehicle_reg:
            return jsonify(v)

## Rent a specific vehicle
## curl "http://localhost:5000/cars/rent?reg=AW69DVJ"
@app.route("/cars/rent", methods=["GET"])
def rent_vehicle():
    vehicle_reg = request.args.get("reg")
    for v in vehicles:
        if v["vrm"] == vehicle_reg:
            v["status"] = "RENTED"
            save_vehicles()
            return jsonify({"message": "Vehicle rented successfully"})

## Return a specific vehicle 
## curl "http://localhost:5000/cars/return?reg=AW69DVJ"
@app.route("/cars/return", methods=["GET"])
def return_vehicle():
    vehicle_reg = request.args.get("reg")
    for v in vehicles:
        if v["vrm"] == vehicle_reg:
            v["status"] = "AVAILABLE"
            save_vehicles()
            return jsonify({"message": "Vehicle returned successfully"})

## Add a new vehicle to the rental fleet 
## curl "http://localhost:5000/cars/add?id=501&make=Ford&model=Fiesta&colour=Grey&vin=B2IJ49B2B3UYIANSI&year=2018&vrm=654321&category=Compact&numberSeats=5&dayRate=50&status=AVAILABLE&fuelEconomy=29.5&branch=Luton"
@app.route("/cars/add", methods=["GET"])
def add_vehicle():
    new_vehicle = {
        "id": request.args.get("id"),
        "make": request.args.get("make"),
        "model": request.args.get("model"),
        "colour": request.args.get("colour"),
        "vin": request.args.get("vin"),
        "year": request.args.get("year"),
        "vrm": request.args.get("vrm"),
        "category": request.args.get("category"),
        "numberSeats": request.args.get("numberSeats"),
        "dayRate": request.args.get("dayRate"),
        "status": request.args.get("status", "AVAILABLE"),
        "fuelEconomy": request.args.get("fuelEconomy"),
        "branch": request.args.get("branch")
    }
    vehicles.append(new_vehicle)
    save_vehicles()
    return jsonify({"message": "Vehicle added successfully"})

## Remove a specific vehicle from the rental fleet 
## curl "http://localhost:5000/cars/remove?reg=AW69DVJ"
@app.route("/cars/remove", methods=["GET"])
def remove_vehicle():
    vehicle_reg = request.args.get("reg")
    global vehicles
    vehicles = [v for v in vehicles if v["vrm"] != vehicle_reg]
    save_vehicles()
    return jsonify({"message": "Vehicle removed successfully"})

## Show all vehicles
## curl "http://localhost:5000/cars/all"
@app.route("/cars/all", methods=["GET"])
def show_all_vehicle():
            return jsonify(vehicles)

## Show all vehicles available to rent
## curl "http://localhost:5000/cars/available"
@app.route("/cars/available", methods=["GET"])
def show_available():
            available_vehicles = []
            for v in vehicles:
                if v["status"] == "AVAILABLE":
                    available_vehicles.append(v)
            return jsonify(available_vehicles)

## Show all vehicles by branch
## curl "http://localhost:5000/cars/branch"
@app.route("/cars/branch", methods=["GET"])
def show_branch():
            branches = {}
            for v in vehicles:
                branch = v["branch"]
                if branch not in branches:
                    branches[branch] = []
                branches[branch].append(v)
            return jsonify(branches)

if __name__ == '__main__':
    load_vehicles()
    app.run(debug=True)

## Additional Endpoints
