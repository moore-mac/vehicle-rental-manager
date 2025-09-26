from flask import Blueprint, jsonify, request
import utils.data_handler as data

analytics_bp = Blueprint("analytics", __name__)


## Rental Utilisation for a given branch
## curl "http://localhost:5000/analytics/rental-utilisation-by-branch?branch=Manchester"
@analytics_bp.route("/analytics/rental-utilisation-by-branch", methods=["GET"])
def rental_utilisation():
    branch = request.args.get("branch")
    if not branch:
        return jsonify({"error": "branch parameter is required"}), 400

    total = 0
    rented = 0

    for v in data.vehicles:
        if v.get("branch") == branch:
            total += 1
            if (v.get("status") or "").upper() == "RENTED":
                rented += 1

    utilisation = round((rented / total) * 100) if total > 0 else 0

    return jsonify([{"group": "value", "value": utilisation}])


## Vehicle Status Breakdown for a Branch
## curl "http://localhost:5000/analytics/status-by-branch?branch=Manchester"
@analytics_bp.route("/analytics/status-by-branch", methods=["GET"])
def status_by_branch():
    branch = request.args.get("branch")
    if not branch:
        return jsonify({"error": "branch parameter is required"}), 400

    breakdown = {}
    for v in data.vehicles:
        if v.get("branch") == branch:
            status = v.get("status", "UNKNOWN")
            breakdown[status] = breakdown.get(status, 0) + 1

    results = [
        {
            "group": status,
            "value": count,
        }
        for status, count in breakdown.items()
    ]

    return jsonify(results)


## Vehicle Category Breakdown for a Branch
## curl "http://localhost:5000/analytics/category-by-branch?branch=Manchester"
@analytics_bp.route("/analytics/category-by-branch", methods=["GET"])
def category_by_branch():
    branch = request.args.get("branch")
    if not branch:
        return jsonify({"error": "branch parameter is required"}), 400

    breakdown = {}
    for v in data.vehicles:
        if v.get("branch") == branch:
            category = v.get("category", "UNKNOWN")
            breakdown[category] = breakdown.get(category, 0) + 1

    results = [
        {
            "group": category,
            "value": count,
        }
        for category, count in breakdown.items()
    ]

    return jsonify(results)


## Rented Vehicles by Category for a Branch
## curl "http://localhost:5000/analytics/rented-by-category?branch=Manchester"
@analytics_bp.route("/analytics/rented-by-category", methods=["GET"])
def rented_by_category():
    branch = request.args.get("branch")
    if not branch:
        return jsonify({"error": "branch parameter is required"}), 400

    breakdown = {}
    for v in data.vehicles:
        if v.get("branch") == branch and v.get("status") == "RENTED":
            category = v.get("category", "UNKNOWN")
            breakdown[category] = breakdown.get(category, 0) + 1

    results = [
        {
            "group": category,
            "value": count,
        }
        for category, count in breakdown.items()
    ]

    return jsonify(results)


## Percentage of Vehicles with Issues (Damaged or Service Required) in a Branch
## curl "http://localhost:5000/analytics/issues-percentage?branch=Bristol"
@analytics_bp.route("/analytics/issues-percentage", methods=["GET"])
def issues_percentage():
    branch = request.args.get("branch")

    if not branch:
        return jsonify({"error": "Branch parameter is required"}), 400

    total = 0
    issues = 0

    for v in data.vehicles:
        if v.get("branch") == branch:
            total += 1
            if v.get("status") in ["DAMAGED", "SERVICEREQ"]:
                issues += 1

    percentage = round((issues / total) * 100) if total > 0 else 0

    results = [
        {
            "group": "",
            "value": percentage,
        }
    ]

    return jsonify(results)


## Get overall fleet analytics
## curl "http://localhost:5000/analytics/fleet"
@analytics_bp.route("/analytics/fleet", methods=["GET"])
def get_fleet_analytics():
    total_vehicles = len(data.vehicles)
    available_count = sum(1 for v in data.vehicles if v["status"] == "AVAILABLE")
    rented_count = sum(1 for v in data.vehicles if v["status"] == "RENTED")

    # Calculate fleet composition
    makes_count = {}
    categories_count = {}
    branch_stats = {}

    for v in data.vehicles:
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
            sum(float(v["dayRate"]) for v in data.vehicles if v["dayRate"])
            / total_vehicles
        )
    except (ValueError, ZeroDivisionError):
        avg_day_rate = 0

    makes_list = [
        {"name": make, "value": count, "showLabel": True}
        for make, count in makes_count.items()
    ]
    categories_list = [
        {
            "group": category,
            "value": count,
        }
        for category, count in categories_count.items()
    ]

    return jsonify(
        {
            "summary": {
                "total_vehicles": total_vehicles,
                "available_vehicles": available_count,
                "rented_vehicles": rented_count,
                "utilisation_rate": (
                    (rented_count / total_vehicles * 100) if total_vehicles > 0 else 0
                ),
                "average_day_rate": round(avg_day_rate, 2),
            },
            "fleet_composition": {
                "by_make": makes_list,
                "by_category": categories_list,
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

    branch_vehicles = [v for v in data.vehicles if v["branch"] == branch_name]
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
            "utilisation_rate": (rented / total * 100) if total > 0 else 0,
            "average_day_rate": round(avg_day_rate, 2),
            "category_distribution": categories,
        }
    )


## Get rental analytics across all branches
## curl "http://localhost:5000/analytics/rentals"
@analytics_bp.route("/analytics/rentals", methods=["GET"])
def get_rental_analytics():
    rented_vehicles = [v for v in data.vehicles if v["status"] == "RENTED"]
    current_rentals = len(rented_vehicles)
    total_vehicles = len(data.vehicles)

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
