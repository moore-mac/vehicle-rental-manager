import csv

# Initialize global variables
vehicles = []
customers = []


def load_customers():
    # Load customers from CSV file
    global customers
    try:
        with open("customer.csv", "r") as f:
            reader = csv.DictReader(f)
            customers = list(reader)
    except FileNotFoundError:
        customers = []


def save_customers():
    # Save customers to CSV file
    if customers:
        with open("customer.csv", "w", newline="") as f:
            writer = csv.DictWriter(f, fieldnames=customers[0].keys())
            writer.writeheader()
            writer.writerows(customers)


def load_vehicles():
    global vehicles
    with open("data/vehicle.csv", "r") as f:
        reader = csv.DictReader(f)
        vehicles = list(reader)


def save_vehicles():
    with open("data/vehicle.csv", "w", newline="") as f:
        if vehicles:
            writer = csv.DictWriter(f, fieldnames=vehicles[0].keys())
            writer.writeheader()
            writer.writerows(vehicles)
