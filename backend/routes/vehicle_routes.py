from flask import Blueprint, jsonify, request
import utils.data_handler as data

vehicle_bp = Blueprint("vehicles", __name__)


## Show details of specific vehicle by car reg
## curl "http://localhost:5000/cars/show?reg=AW69DVJ"
@vehicle_bp.route("/cars/show", methods=["GET"])
def get_reg():
    vehicle_reg = request.args.get("reg")
    for v in data.vehicles:
        if v["vrm"].strip() == vehicle_reg:
            return jsonify(v)
    return jsonify({"error": "Vehicle not found"}), 404


## Rent a specific vehicle
## curl "http://localhost:5000/cars/rent?reg=AW69DVJ"
@vehicle_bp.route("/cars/rent", methods=["PUT"])
def rent_vehicle():
    vehicle_reg = request.args.get("reg")
    for v in data.vehicles:
        if v["vrm"].strip() == vehicle_reg:
            v["status"] = "RENTED"
            data.save_vehicles()
            return jsonify(v)
    return jsonify({"error": "Vehicle not found"}), 404


## Return a specific vehicle
## curl "http://localhost:5000/cars/return?reg=AW69DVJ"
@vehicle_bp.route("/cars/return", methods=["PUT"])
def return_vehicle():
    vehicle_reg = request.args.get("reg")
    for v in data.vehicles:
        if v["vrm"].strip() == vehicle_reg:
            v["status"] = "AVAILABLE"
            data.save_vehicles()
            return jsonify(v)
    return jsonify({"error": "Vehicle not found"}), 404


## Add a new vehicle to the rental fleet
## curl "http://localhost:5000/cars/add?id=501&make=Ford&model=Fiesta&colour=Grey&vin=B2IJ49B2B3UYIANSI&year=2018&vrm=654321&category=Compact&numberSeats=5&dayRate=50&status=AVAILABLE&fuelEconomy=29.5&branch=Luton"
@vehicle_bp.route("/cars/add", methods=["POST"])
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
    data.vehicles.append(new_vehicle)
    data.save_vehicles()
    return jsonify({"message": "Vehicle added successfully"})


## Remove a specific vehicle from the rental fleet (by ID)
## curl "http://localhost:5000/cars/remove?id=123"
@vehicle_bp.route("/cars/remove", methods=["POST"])
def remove_vehicle():
    vehicle_id = request.args.get("id")
    if not vehicle_id:
        return jsonify({"error": "Missing 'id' parameter"}), 400

    before_count = len(data.vehicles)
    data.vehicles[:] = [v for v in data.vehicles if str(v.get("id")) != str(vehicle_id)]
    after_count = len(data.vehicles)

    if before_count == after_count:
        return jsonify({"message": f"No vehicle found with id={vehicle_id}"}), 404

    data.save_vehicles()
    return jsonify({"message": f"Vehicle {vehicle_id} removed successfully"})


## Remove multiple vehicles from the rental fleet (by ID)
## curl -X POST "http://localhost:5000/cars/remove-batch"
## {"ids": [1, 2, 3]}
@vehicle_bp.route("/cars/remove-batch", methods=["POST"])
def remove_vehicles_batch():
    payload = request.get_json(force=True, silent=True)
    if not payload or "ids" not in payload:
        return jsonify({"error": "Missing 'ids' list in request body"}), 400

    ids_to_remove = set(str(i) for i in payload["ids"])
    if not ids_to_remove:
        return jsonify({"error": "Empty 'ids' list"}), 400

    before_count = len(data.vehicles)
    data.vehicles[:] = [
        v for v in data.vehicles if str(v.get("id")) not in ids_to_remove
    ]
    after_count = len(data.vehicles)
    removed_count = before_count - after_count

    if removed_count == 0:
        return jsonify({"message": "No vehicles matched given IDs"}), 404

    data.save_vehicles()

    return jsonify(
        {
            "message": f"Removed {removed_count} vehicles successfully",
            "removed_count": removed_count,
            "remaining": after_count,
        }
    )


## Show all vehicles
## curl "http://localhost:5000/cars/all"
@vehicle_bp.route("/cars/all", methods=["GET"])
def show_all_vehicle():
    return jsonify(data.vehicles)


## Show all vehicles available to rent
## curl "http://localhost:5000/cars/available"
@vehicle_bp.route("/cars/available", methods=["GET"])
def show_available():
    available_vehicles = []
    for v in data.vehicles:
        if v["status"] == "AVAILABLE":
            available_vehicles.append(v)
    return jsonify(available_vehicles)


## Show all vehicles by branch
## curl "http://localhost:5000/cars/branch"
@vehicle_bp.route("/cars/branch", methods=["GET"])
def show_branch():
    branches = {}
    for v in data.vehicles:
        branch = v["branch"]
        if branch not in branches:
            branches[branch] = []
        branches[branch].append(v)
    return jsonify(branches)


## Additional Endpoints


## Get vehicles by category
## curl "http://localhost:5000/cars/category?category=Compact"
@vehicle_bp.route("/cars/category", methods=["GET"])
def get_vehicles_by_category():
    category = request.args.get("category")
    category_vehicles = [v for v in data.vehicles if v["category"] == category]
    return jsonify(category_vehicles)


## Get list of categories
## curl "http://localhost:5000/cars/category-list"
@vehicle_bp.route("/cars/category-list", methods=["GET"])
def get_categories():
    categories = []
    for v in data.vehicles:
        if v["category"] not in categories:
            categories.append(v["category"])
    return jsonify(categories)


## Get list of branches
## curl "http://localhost:5000/cars/branch-list"
@vehicle_bp.route("/cars/branch-list", methods=["GET"])
def get_branches():
    branches = []
    for v in data.vehicles:
        if v["branch"] not in branches:
            branches.append(v["branch"])
    return jsonify(branches)


## Search vehicles by various criteria
## curl "http://localhost:5000/cars/search?query=Toyota&branch=London&status=AVAILABLE&limit=10"
@vehicle_bp.route("/cars/search", methods=["GET"])
def search_vehicles():
    query = request.args.get("query", "").strip().lower()
    branch = request.args.get("branch")
    status = request.args.get("status")
    category = request.args.get("category")
    max_price = request.args.get("max_price")
    limit = request.args.get("limit", type=int)

    results = []
    for vehicle in data.vehicles:
        matches = True

        if query:
            search_fields = ["make", "model", "colour", "vrm", "category", "branch"]
            text_match = any(
                query in str(vehicle.get(f, "")).lower() for f in search_fields
            )
            matches = matches and text_match

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
            except (ValueError, TypeError):
                continue

        if matches:
            results.append(vehicle)

    # Apply limit if specified
    if limit is not None and limit > 0:
        results = results[:limit]

    filters_used = {}
    if query:
        filters_used["query"] = query
    if branch:
        filters_used["branch"] = branch
    if status:
        filters_used["status"] = status
    if category:
        filters_used["category"] = category
    if max_price:
        filters_used["max_price"] = max_price
    if limit:
        filters_used["limit"] = limit

    return jsonify(
        {
            "results": results,
            "count": len(results),
            "filters_used": filters_used,
        }
    )
