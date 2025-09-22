from flask import Flask, jsonify, request
import csv
import os

app = Flask(__name__)

# Initialize global variables
vehicles = []
customers = []

def load_customers():
    """Load customers from CSV file"""
    global customers
    try:
        with open('customer.csv', 'r') as f:
            reader = csv.DictReader(f)
            customers = list(reader)
    except FileNotFoundError:
        customers = []

def save_customers():
    """Save customers to CSV file"""
    if customers:
        with open('customer.csv', 'w', newline='') as f:
            writer = csv.DictWriter(f, fieldnames=customers[0].keys())
            writer.writeheader()
            writer.writerows(customers)

def load_vehicles():
    global vehicles
    with open('vehicle.csv', 'r') as f:
        reader = csv.DictReader(f)
        vehicles = list(reader)

def save_vehicles():
    with open('vehicle.csv', 'w', newline='') as f:
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
    return jsonify({"error": "Vehicle not found"}), 404

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
## curl "http://localhost:5000/cars/add?id=501&make=Ford&model=Fiesta&colour=Grey&vin=123456&year=2018&vrm=654321&category=Compact&numberSeats=5&dayRate=50&status=AVAILABLE&fuelEconomy=29.5&branch=Luton"
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

## Edit a vehicle's details
## curl "http://localhost:5000/cars/edit?reg=AW69DVJ&colour=Blue&dayRate=60&branch=Manchester"
@app.route("/cars/edit", methods=["GET", "POST", "PUT"])
def edit_vehicle():
    vehicle_reg = request.args.get("reg")
    if not vehicle_reg:
        return jsonify({"error": "Registration number required"}), 400
    
    # Fields that are allowed to be updated
    allowed_fields = ["colour", "dayRate", "status", "branch", "category", "numberSeats"]
    updates = {k: request.args.get(k) for k in allowed_fields if request.args.get(k)}
    
    if not updates:
        return jsonify({"error": "No valid fields to update"}), 400
    
    for v in vehicles:
        if v["vrm"] == vehicle_reg:
            v.update(updates)
            save_vehicles()
            return jsonify({"message": "Vehicle updated successfully", "vehicle": v})
    
    return jsonify({"error": "Vehicle not found"}), 404

## Batch edit multiple vehicles
## curl -X POST -H "Content-Type: application/json" -d '[{"reg":"AW69DVJ","updates":{"colour":"Red"}},{"reg":"JA82VXV","updates":{"dayRate":"75"}}]' "http://localhost:5000/cars/batch-edit"
@app.route("/cars/batch-edit", methods=["POST", "PUT"])
def batch_edit_vehicles():
    updates_list = request.get_json()
    if not updates_list:
        return jsonify({"error": "No updates provided"}), 400
    
    allowed_fields = ["colour", "dayRate", "status", "branch", "category", "numberSeats"]
    results = []
    
    for update in updates_list:
        if "reg" not in update or "updates" not in update:
            return jsonify({"error": "Each update must contain 'reg' and 'updates' fields"}), 400
        
        vehicle_reg = update["reg"]
        updates = {k: v for k, v in update["updates"].items() if k in allowed_fields}
        
        if not updates:
            results.append({
                "reg": vehicle_reg,
                "status": "error",
                "message": "No valid fields to update"
            })
            continue
        
        vehicle_found = False
        for v in vehicles:
            if v["vrm"] == vehicle_reg:
                v.update(updates)
                results.append({
                    "reg": vehicle_reg,
                    "status": "success",
                    "vehicle": v
                })
                vehicle_found = True
                break
        
        if not vehicle_found:
            results.append({
                "reg": vehicle_reg,
                "status": "error",
                "message": "Vehicle not found"
            })
    
    if any(r["status"] == "success" for r in results):
        save_vehicles()
    
    return jsonify({"results": results})

## Bulk add multiple vehicles
## curl -X POST -H "Content-Type: application/json" -d '[{"id":"501","make":"Ford","model":"Fiesta","vrm":"ABC123"},{"id":"502","make":"Toyota","model":"Corolla","vrm":"XYZ789"}]' "http://localhost:5000/cars/bulk-add"
@app.route("/cars/bulk-add", methods=["POST"])
def bulk_add_vehicles():
    new_vehicles = request.get_json()
    if not new_vehicles:
        return jsonify({"error": "No vehicles provided"}), 400
    
    required_fields = ["id", "make", "model", "vrm"]
    results = []
    added_count = 0
    
    for vehicle in new_vehicles:
        # Check required fields
        missing_fields = [field for field in required_fields if field not in vehicle]
        if missing_fields:
            results.append({
                "vrm": vehicle.get("vrm", "Unknown"),
                "status": "error",
                "message": f"Missing required fields: {', '.join(missing_fields)}"
            })
            continue
        
        # Check for duplicate VRM
        if any(v["vrm"] == vehicle["vrm"] for v in vehicles):
            results.append({
                "vrm": vehicle["vrm"],
                "status": "error",
                "message": "Vehicle with this registration already exists"
            })
            continue
        
        # Add default values
        vehicle.setdefault("status", "AVAILABLE")
        vehicle.setdefault("branch", "Main Branch")
        vehicle.setdefault("category", "Standard")
        
        vehicles.append(vehicle)
        results.append({
            "vrm": vehicle["vrm"],
            "status": "success",
            "message": "Vehicle added successfully"
        })
        added_count += 1
    
    if added_count > 0:
        save_vehicles()
    
    return jsonify({"results": results, "added_count": added_count})

## Search vehicles by various criteria
## curl "http://localhost:5000/cars/search?query=Toyota&branch=London&status=AVAILABLE"
@app.route("/cars/search", methods=["GET"])
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
                matches = matches and float(vehicle.get("dayRate", 0)) <= float(max_price)
            except ValueError:
                continue
        
        if matches:
            results.append(vehicle)
    
    return jsonify({
        "results": results,
        "count": len(results),
        "filters_used": {
            "query": query if query else None,
            "branch": branch,
            "status": status,
            "category": category,
            "max_price": max_price
        }
    })

## Get fleet analytics
## curl "http://localhost:5000/analytics/fleet"
@app.route("/analytics/fleet", methods=["GET"])
def get_fleet_analytics():
    total_vehicles = len(vehicles)
    available_count = sum(1 for v in vehicles if v["status"] == "AVAILABLE")
    rented_count = sum(1 for v in vehicles if v["status"] == "RENTED")
    
    # Calculate fleet composition
    makes_count = {}
    categories_count = {}
    branch_stats = {}
    
    for v in vehicles:
        # Count by make
        makes_count[v["make"]] = makes_count.get(v["make"], 0) + 1
        
        # Count by category
        categories_count[v["category"]] = categories_count.get(v["category"], 0) + 1
        
        # Branch statistics
        branch = v["branch"]
        if branch not in branch_stats:
            branch_stats[branch] = {
                "total": 0,
                "available": 0,
                "rented": 0
            }
        
        branch_stats[branch]["total"] += 1
        if v["status"] == "AVAILABLE":
            branch_stats[branch]["available"] += 1
        elif v["status"] == "RENTED":
            branch_stats[branch]["rented"] += 1
    
    # Calculate average day rate
    try:
        avg_day_rate = sum(float(v["dayRate"]) for v in vehicles if v["dayRate"]) / total_vehicles
    except (ValueError, ZeroDivisionError):
        avg_day_rate = 0
    
    return jsonify({
        "summary": {
            "total_vehicles": total_vehicles,
            "available_vehicles": available_count,
            "rented_vehicles": rented_count,
            "utilization_rate": (rented_count / total_vehicles * 100) if total_vehicles > 0 else 0,
            "average_day_rate": round(avg_day_rate, 2)
        },
        "fleet_composition": {
            "by_make": makes_count,
            "by_category": categories_count
        },
        "branch_performance": branch_stats
    })

## Get branch analytics
## curl "http://localhost:5000/analytics/branch?name=London"
@app.route("/analytics/branch", methods=["GET"])
def get_branch_analytics():
    branch_name = request.args.get("name")
    if not branch_name:
        return jsonify({"error": "Branch name is required"}), 400
    
    branch_vehicles = [v for v in vehicles if v["branch"] == branch_name]
    if not branch_vehicles:
        return jsonify({"error": "Branch not found"}), 404
    
    total = len(branch_vehicles)
    available = sum(1 for v in branch_vehicles if v["status"] == "AVAILABLE")
    rented = sum(1 for v in branch_vehicles if v["status"] == "RENTED")
    
    # Calculate category distribution
    categories = {}
    for v in branch_vehicles:
        categories[v["category"]] = categories.get(v["category"], 0) + 1
    
    # Calculate average day rate
    try:
        avg_day_rate = sum(float(v["dayRate"]) for v in branch_vehicles if v["dayRate"]) / total
    except (ValueError, ZeroDivisionError):
        avg_day_rate = 0
    
    return jsonify({
        "branch_name": branch_name,
        "total_vehicles": total,
        "available_vehicles": available,
        "rented_vehicles": rented,
        "utilization_rate": (rented / total * 100) if total > 0 else 0,
        "average_day_rate": round(avg_day_rate, 2),
        "category_distribution": categories
    })

## Get rental analytics
## curl "http://localhost:5000/analytics/rentals"
@app.route("/analytics/rentals", methods=["GET"])
def get_rental_analytics():
    rented_vehicles = [v for v in vehicles if v["status"] == "RENTED"]
    current_rentals = len(rented_vehicles)
    total_vehicles = len(vehicles)

    # Calculate rental statistics by category
    rentals_by_category = {}
    for v in rented_vehicles:
        category = v["category"]
        rentals_by_category[category] = rentals_by_category.get(category, 0) + 1

    # Calculate rental statistics by branch
    rentals_by_branch = {}
    for v in rented_vehicles:
        branch = v["branch"]
        rentals_by_branch[branch] = rentals_by_branch.get(branch, 0) + 1

    return jsonify({
        "current_rentals": current_rentals,
        "rental_rate": (current_rentals / total_vehicles * 100) if total_vehicles > 0 else 0,
        "rentals_by_category": rentals_by_category,
        "rentals_by_branch": rentals_by_branch
    })

## Customer Account Management Endpoints ##

## Get all customers
## curl "http://localhost:5000/customers/all"
@app.route("/customers/all", methods=["GET"])
def get_all_customers():
    return jsonify(customers)

## Get customer by ID
## curl "http://localhost:5000/customers/show?id=12345"
@app.route("/customers/show", methods=["GET"])
def get_customer():
    customer_id = request.args.get("id")
    if not customer_id:
        return jsonify({"error": "Customer ID required"}), 400
    
    for customer in customers:
        if customer["id"] == customer_id:
            return jsonify(customer)
    
    return jsonify({"error": "Customer not found"}), 404

## Add new customer
## curl "http://localhost:5000/customers/add?id=12345&name=John%20Doe&email=john@example.com&phone=1234567890&license=DL12345"
@app.route("/customers/add", methods=["GET"])
def add_customer():
    required_fields = ["id", "name", "email", "license"]
    for field in required_fields:
        if not request.args.get(field):
            return jsonify({"error": f"Missing required field: {field}"}), 400
    
    # Check for duplicate customer ID
    if any(c["id"] == request.args.get("id") for c in customers):
        return jsonify({"error": "Customer with this ID already exists"}), 400
    
    new_customer = {
        "id": request.args.get("id"),
        "name": request.args.get("name"),
        "email": request.args.get("email"),
        "phone": request.args.get("phone", ""),
        "license": request.args.get("license"),
        "status": request.args.get("status", "ACTIVE"),
        "rentals": "0"
    }
    
    customers.append(new_customer)
    save_customers()
    return jsonify({"message": "Customer added successfully", "customer": new_customer}), 201

## Update customer details
## curl "http://localhost:5000/customers/update?id=12345&phone=9876543210&status=INACTIVE"
@app.route("/customers/update", methods=["GET"])
def update_customer():
    customer_id = request.args.get("id")
    if not customer_id:
        return jsonify({"error": "Customer ID required"}), 400
    
    allowed_fields = ["name", "email", "phone", "license", "status"]
    updates = {k: request.args.get(k) for k in allowed_fields if request.args.get(k)}
    
    if not updates:
        return jsonify({"error": "No valid fields to update"}), 400
    
    for customer in customers:
        if customer["id"] == customer_id:
            customer.update(updates)
            save_customers()
            return jsonify({"message": "Customer updated successfully", "customer": customer})
    
    return jsonify({"error": "Customer not found"}), 404

## Remove customer
## curl "http://localhost:5000/customers/remove?id=12345"
@app.route("/customers/remove", methods=["GET"])
def remove_customer():
    customer_id = request.args.get("id")
    if not customer_id:
        return jsonify({"error": "Customer ID required"}), 400
    
    initial_count = len(customers)
    customers[:] = [c for c in customers if c["id"] != customer_id]
    
    if len(customers) == initial_count:
        return jsonify({"error": "Customer not found"}), 404
    
    save_customers()
    return jsonify({"message": "Customer removed successfully"})

## Search customers
## curl "http://localhost:5000/customers/search?query=John"
@app.route("/customers/search", methods=["GET"])
def search_customers():
    query = request.args.get("query", "").lower()
    status = request.args.get("status")
    
    results = []
    for customer in customers:
        if not query and not status:
            continue
        
        matches = True
        
        if query:
            text_match = any(
                query in str(customer.get(field, "")).lower()
                for field in ["name", "email", "phone", "license"]
            )
            matches = matches and text_match
        
        if status:
            matches = matches and customer.get("status") == status
        
        if matches:
            results.append(customer)
    
    return jsonify({
        "results": results,
        "count": len(results)
    })

## Initialize data
def initialize():
    """Load both vehicles and customers when the app starts"""
    with app.app_context():
        load_vehicles()
        load_customers()

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