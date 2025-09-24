from flask import Blueprint, jsonify, request
from models.data import vehicles

analytics_bp = Blueprint('analytics', __name__)

## Get fleet analytics
## curl "http://localhost:5000/analytics/fleet"
@analytics_bp.route("/analytics/fleet", methods=["GET"])
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
            branch_stats[branch] = {"total": 0, "available": 0, "rented": 0}

        branch_stats[branch]["total"] += 1
        if v["status"] == "AVAILABLE":
            branch_stats[branch]["available"] += 1
        elif v["status"] == "RENTED":
            branch_stats[branch]["rented"] += 1

    # Calculate average day rate
    try:
        avg_day_rate = (
            sum(float(v["dayRate"]) for v in vehicles if v["dayRate"]) / total_vehicles
        )
    except (ValueError, ZeroDivisionError):
        avg_day_rate = 0

    return jsonify(
        {
            "summary": {
                "total_vehicles": total_vehicles,
                "available_vehicles": available_count,
                "rented_vehicles": rented_count,
                "utilization_rate": (
                    (rented_count / total_vehicles * 100) if total_vehicles > 0 else 0
                ),
                "average_day_rate": round(avg_day_rate, 2),
            },
            "fleet_composition": {
                "by_make": makes_count,
                "by_category": categories_count,
            },
            "branch_performance": branch_stats,
        }
    )


## Get branch analytics
## curl "http://localhost:5000/analytics/branch?name=London"
@analytics_bp.route("/analytics/branch", methods=["GET"])
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
        avg_day_rate = (
            sum(float(v["dayRate"]) for v in branch_vehicles if v["dayRate"]) / total
        )
    except (ValueError, ZeroDivisionError):
        avg_day_rate = 0

    return jsonify(
        {
            "branch_name": branch_name,
            "total_vehicles": total,
            "available_vehicles": available,
            "rented_vehicles": rented,
            "utilization_rate": (rented / total * 100) if total > 0 else 0,
            "average_day_rate": round(avg_day_rate, 2),
            "category_distribution": categories,
        }
    )


## Get rental analytics
## curl "http://localhost:5000/analytics/rentals"
@analytics_bp.route("/analytics/rentals", methods=["GET"])
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

    return jsonify(
        {
            "current_rentals": current_rentals,
            "rental_rate": (
                (current_rentals / total_vehicles * 100) if total_vehicles > 0 else 0
            ),
            "rentals_by_category": rentals_by_category,
            "rentals_by_branch": rentals_by_branch,
        }
    )
