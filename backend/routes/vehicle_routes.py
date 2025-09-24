from flask import Blueprint, jsonify, request
from models.data import vehicles, save_vehicles

vehicle_bp = Blueprint('vehicles', __name__)

## Show details of specific vehicle by car reg
## curl "http://localhost:5000/cars/show?reg=AW69DVJ"
@vehicle_bp.route("/cars/show", methods=["GET"])
def get_reg():
    vehicle_reg = request.args.get("reg")
    for v in vehicles:
        if v["vrm"] == vehicle_reg:
            return jsonify(v)


## Rent a specific vehicle
## curl "http://localhost:5000/cars/rent?reg=AW69DVJ"
@vehicle_bp.route("/cars/rent", methods=["GET"])
def rent_vehicle():
    vehicle_reg = request.args.get("reg")
    for v in vehicles:
        if v["vrm"] == vehicle_reg:
            v["status"] = "RENTED"
            save_vehicles()
            return jsonify({"message": "Vehicle rented successfully"})


## Return a specific vehicle
## curl "http://localhost:5000/cars/return?reg=AW69DVJ"
@vehicle_bp.route("/cars/return", methods=["GET"])
def return_vehicle():
    vehicle_reg = request.args.get("reg")
    for v in vehicles:
        if v["vrm"] == vehicle_reg:
            v["status"] = "AVAILABLE"
            save_vehicles()
            return jsonify({"message": "Vehicle returned successfully"})


## Add a new vehicle to the rental fleet
## curl "http://localhost:5000/cars/add?id=501&make=Ford&model=Fiesta&colour=Grey&vin=B2IJ49B2B3UYIANSI&year=2018&vrm=654321&category=Compact&numberSeats=5&dayRate=50&status=AVAILABLE&fuelEconomy=29.5&branch=Luton"
@vehicle_bp.route("/cars/add", methods=["GET"])
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
        "branch": request.args.get("branch"),
    }
    vehicles.append(new_vehicle)
    save_vehicles()
    return jsonify({"message": "Vehicle added successfully"})


## Remove a specific vehicle from the rental fleet
## curl "http://localhost:5000/cars/remove?reg=AW69DVJ"
@vehicle_bp.route("/cars/remove", methods=["GET"])
def remove_vehicle():
    vehicle_reg = request.args.get("reg")
    global vehicles
    vehicles = [v for v in vehicles if v["vrm"] != vehicle_reg]
    save_vehicles()
    return jsonify({"message": "Vehicle removed successfully"})


## Show all vehicles
## curl "http://localhost:5000/cars/all"
@vehicle_bp.route("/cars/all", methods=["GET"])
def show_all_vehicle():
    return jsonify(vehicles)


## Show all vehicles available to rent
## curl "http://localhost:5000/cars/available"
@vehicle_bp.route("/cars/available", methods=["GET"])
def show_available():
    available_vehicles = []
    for v in vehicles:
        if v["status"] == "AVAILABLE":
            available_vehicles.append(v)
    return jsonify(available_vehicles)


@vehicle_bp.route("/cars/fetch_by_branch", methods=["GET"])
def fetch_by_branch():
    branch = request.args.get("branch")

    if not branch:
        return jsonify({"error": "branch query parameter is required"}), 400

    filtered_vehicles = [v for v in vehicles if v["branch"] == branch]

    return jsonify(filtered_vehicles)


## Additional Endpoints


## Get list of branches
## curl "http://localhost:5000/cars/branch-list"
@vehicle_bp.route("/cars/branch-list", methods=["GET"])
def get_branches():
    branches = []
    for v in vehicles:
        if v["branch"] not in branches:
            branches.append(v["branch"])
    return jsonify(branches)


## Search vehicles by various criteria
## curl "http://localhost:5000/cars/search?query=Toyota&branch=London&status=AVAILABLE"
@vehicle_bp.route("/cars/search", methods=["GET"])
def search_vehicles():
    query = request.args.get("query", "").lower()
    branch = request.args.get("branch")
    status = request.args.get("status")
    category = request.args.get("category")
    max_price = request.args.get("max_price")

    results = []
    for vehicle in vehicles:
        # If no search criteria provided, skip this vehicle
        if not any([query, branch, status, category, max_price]):
            continue

        matches = True

        # Check text search across multiple fields
        if query:
            text_match = False
            search_fields = ["make", "model", "colour", "vrm", "category", "branch"]
            for field in search_fields:
                if query in str(vehicle.get(field, "")).lower():
                    text_match = True
                    break
            matches = matches and text_match

        # Check exact matches
        if branch:
            matches = matches and vehicle.get("branch") == branch
        if status:
            matches = matches and vehicle.get("status") == status
        if category:
            matches = matches and vehicle.get("category") == category
        if max_price:
            try:
                matches = matches and float(vehicle.get("dayRate", 0)) <= float(
                    max_price
                )
            except ValueError:
                continue

        if matches:
            results.append(vehicle)

    return jsonify(
        {
            "results": results,
            "count": len(results),
            "filters_used": {
                "query": query if query else None,
                "branch": branch,
                "status": status,
                "category": category,
                "max_price": max_price,
            },
        }
    )
