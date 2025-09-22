import unittest
import json
import requests
from api import app
import csv

class VehicleRentalAPITest(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()
        self.base_url = 'http://localhost:5000'
        
        # Test vehicle data
        self.test_vehicle = {
            "id": "999",
            "make": "Tesla",
            "model": "Model 3",
            "colour": "Red",
            "vin": "TEST123456",
            "year": "2023",
            "vrm": "TEST123",
            "category": "Electric",
            "numberSeats": "5",
            "dayRate": "75",
            "status": "AVAILABLE",
            "fuelEconomy": "N/A",
            "branch": "London"
        }
        
        # Test data for bulk operations
        self.bulk_vehicles = [
            {
                "id": "901",
                "make": "BMW",
                "model": "i3",
                "colour": "Blue",
                "vin": "BULK123456",
                "year": "2023",
                "vrm": "BULK123",
                "category": "Electric",
                "numberSeats": "4",
                "dayRate": "65",
                "status": "AVAILABLE",
                "fuelEconomy": "N/A",
                "branch": "Manchester"
            },
            {
                "id": "902",
                "make": "Audi",
                "model": "e-tron",
                "colour": "Black",
                "vin": "BULK789012",
                "year": "2023",
                "vrm": "BULK789",
                "category": "Electric",
                "numberSeats": "5",
                "dayRate": "85",
                "status": "AVAILABLE",
                "fuelEconomy": "N/A",
                "branch": "London"
            }
        ]

    def test_01_show_vehicle_details(self):
        """Test showing details of a specific vehicle"""
        # First add a test vehicle
        response = self.app.get('/cars/add', query_string=self.test_vehicle)
        self.assertEqual(response.status_code, 200)
        
        # Then retrieve its details
        response = self.app.get(f'/cars/show?reg={self.test_vehicle["vrm"]}')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertEqual(data["vrm"], self.test_vehicle["vrm"])
        self.assertEqual(data["make"], self.test_vehicle["make"])

    def test_02_rent_vehicle(self):
        """Test renting a vehicle"""
        # Attempt to rent the test vehicle
        response = self.app.get(f'/cars/rent?reg={self.test_vehicle["vrm"]}')
        self.assertEqual(response.status_code, 200)
        
        # Verify the vehicle is now rented
        response = self.app.get(f'/cars/show?reg={self.test_vehicle["vrm"]}')
        data = json.loads(response.data)
        self.assertEqual(data["status"], "RENTED")

    def test_03_return_vehicle(self):
        """Test returning a vehicle"""
        # Return the previously rented vehicle
        response = self.app.get(f'/cars/return?reg={self.test_vehicle["vrm"]}')
        self.assertEqual(response.status_code, 200)
        
        # Verify the vehicle is now available
        response = self.app.get(f'/cars/show?reg={self.test_vehicle["vrm"]}')
        data = json.loads(response.data)
        self.assertEqual(data["status"], "AVAILABLE")

    def test_04_edit_vehicle(self):
        """Test editing a vehicle's details"""
        # Add a test vehicle first
        response = self.app.get('/cars/add', query_string=self.test_vehicle)
        self.assertEqual(response.status_code, 200)
        
        # Edit the vehicle
        updates = {
            "reg": self.test_vehicle["vrm"],
            "colour": "Blue",
            "dayRate": "80",
            "branch": "Manchester"
        }
        response = self.app.get('/cars/edit', query_string=updates)
        self.assertEqual(response.status_code, 200)
        
        # Verify changes
        response = self.app.get(f'/cars/show?reg={self.test_vehicle["vrm"]}')
        data = json.loads(response.data)
        self.assertEqual(data["colour"], "Blue")
        self.assertEqual(data["dayRate"], "80")
        self.assertEqual(data["branch"], "Manchester")

    def test_05_batch_edit_vehicles(self):
        """Test batch editing multiple vehicles"""
        # Add test vehicles first
        for vehicle in self.bulk_vehicles:
            response = self.app.get('/cars/add', query_string=vehicle)
            self.assertEqual(response.status_code, 200)
        
        # Batch edit vehicles
        updates = [
            {
                "reg": self.bulk_vehicles[0]["vrm"],
                "updates": {"colour": "Green", "dayRate": "70"}
            },
            {
                "reg": self.bulk_vehicles[1]["vrm"],
                "updates": {"branch": "Birmingham", "status": "AVAILABLE"}
            }
        ]
        response = self.app.post('/cars/batch-edit',
                               data=json.dumps(updates),
                               content_type='application/json')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertEqual(len(data["results"]), 2)
        self.assertEqual(data["results"][0]["status"], "success")
        self.assertEqual(data["results"][1]["status"], "success")

    def test_06_bulk_add_vehicles(self):
        """Test bulk adding vehicles"""
        response = self.app.post('/cars/bulk-add',
                               data=json.dumps(self.bulk_vehicles),
                               content_type='application/json')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertEqual(data["added_count"], 2)
        
        # Verify vehicles were added
        for vehicle in self.bulk_vehicles:
            response = self.app.get(f'/cars/show?reg={vehicle["vrm"]}')
            self.assertEqual(response.status_code, 200)
            data = json.loads(response.data)
            self.assertEqual(data["vrm"], vehicle["vrm"])

    def test_07_search_vehicles(self):
        """Test searching vehicles"""
        # Add test vehicles first
        response = self.app.get('/cars/add', query_string=self.test_vehicle)
        self.assertEqual(response.status_code, 200)
        
        # Test search by make
        response = self.app.get('/cars/search?query=Tesla')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertGreater(len(data["results"]), 0)
        
        # Test search by branch
        response = self.app.get('/cars/search?branch=London')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertGreater(len(data["results"]), 0)
        
        # Test search by status
        response = self.app.get('/cars/search?status=AVAILABLE')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertGreater(len(data["results"]), 0)

    def test_08_fleet_analytics(self):
        """Test fleet analytics endpoint"""
        response = self.app.get('/analytics/fleet')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        
        # Check structure
        self.assertIn("summary", data)
        self.assertIn("fleet_composition", data)
        self.assertIn("branch_performance", data)
        
        # Check summary data
        summary = data["summary"]
        self.assertGreaterEqual(summary["total_vehicles"], 0)
        self.assertGreaterEqual(summary["available_vehicles"], 0)
        self.assertGreaterEqual(summary["rented_vehicles"], 0)
        self.assertGreaterEqual(summary["average_day_rate"], 0)

    def test_09_branch_analytics(self):
        """Test branch analytics endpoint"""
        # Add a test vehicle to ensure branch exists
        response = self.app.get('/cars/add', query_string=self.test_vehicle)
        self.assertEqual(response.status_code, 200)
        
        response = self.app.get(f'/analytics/branch?name={self.test_vehicle["branch"]}')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        
        # Check structure
        self.assertEqual(data["branch_name"], self.test_vehicle["branch"])
        self.assertGreaterEqual(data["total_vehicles"], 1)
        self.assertIn("category_distribution", data)
        self.assertIn("utilization_rate", data)

    def test_10_customer_management(self):
        """Test customer management endpoints"""
        # Test customer data
        test_customer = {
            "id": "C999",
            "name": "John Doe",
            "email": "john@example.com",
            "phone": "1234567890",
            "license": "DL12345"
        }
        
        # Test adding customer
        response = self.app.get('/customers/add', query_string=test_customer)
        self.assertEqual(response.status_code, 201)
        
        # Test getting customer
        response = self.app.get(f'/customers/show?id={test_customer["id"]}')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertEqual(data["name"], test_customer["name"])
        
        # Test updating customer
        updates = {
            "id": test_customer["id"],
            "phone": "9876543210",
            "status": "INACTIVE"
        }
        response = self.app.get('/customers/update', query_string=updates)
        self.assertEqual(response.status_code, 200)
        
        # Test searching customers
        response = self.app.get('/customers/search?query=John')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertGreater(len(data["results"]), 0)
        
        # Test removing customer
        response = self.app.get(f'/customers/remove?id={test_customer["id"]}')
        self.assertEqual(response.status_code, 200)

    def test_11_remove_vehicle(self):
        """Test removing a vehicle"""
        response = self.app.get(f'/cars/remove?reg={self.test_vehicle["vrm"]}')
        self.assertEqual(response.status_code, 200)
        
        # Verify the vehicle is removed
        response = self.app.get(f'/cars/show?reg={self.test_vehicle["vrm"]}')
        self.assertEqual(response.status_code, 404)

    def test_05_show_all_vehicles(self):
        """Test showing all vehicles"""
        response = self.app.get('/cars/all')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertIsInstance(data, list)

    def test_06_show_available_vehicles(self):
        """Test showing available vehicles"""
        response = self.app.get('/cars/available')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertIsInstance(data, list)
        for vehicle in data:
            self.assertEqual(vehicle["status"], "AVAILABLE")

    def test_07_show_rented_vehicles(self):
        """Test showing rented vehicles by branch"""
        response = self.app.get('/cars/branch')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertIsInstance(data, dict)

    def test_08_edit_vehicle(self):
        """Test editing a single vehicle"""
        # Add a test vehicle first
        response = self.app.get('/cars/add', query_string=self.test_vehicle)
        self.assertEqual(response.status_code, 200)
        
        # Edit the vehicle
        updates = {
            "reg": self.test_vehicle["vrm"],
            "colour": "Blue",
            "dayRate": "80",
            "branch": "Manchester",
            "category": "Luxury",
            "status": "AVAILABLE"
        }
        response = self.app.get('/cars/edit', query_string=updates)
        self.assertEqual(response.status_code, 200)
        
        # Verify changes
        response = self.app.get(f'/cars/show?reg={self.test_vehicle["vrm"]}')
        data = json.loads(response.data)
        self.assertEqual(data["colour"], "Blue")
        self.assertEqual(data["dayRate"], "80")
        self.assertEqual(data["branch"], "Manchester")
        self.assertEqual(data["category"], "Luxury")
        self.assertEqual(data["status"], "AVAILABLE")

    def test_09_batch_edit(self):
        """Test batch editing multiple vehicles"""
        # First add test vehicles
        for vehicle in self.bulk_vehicles:
            response = self.app.get('/cars/add', query_string=vehicle)
            self.assertEqual(response.status_code, 200)
        
        # Test batch edit
        updates = [
            {"reg": self.bulk_vehicles[0]["vrm"], "updates": {"colour": "Green", "dayRate": "70"}},
            {"reg": self.bulk_vehicles[1]["vrm"], "updates": {"colour": "Silver", "dayRate": "90"}}
        ]
        response = self.app.put(
            '/cars/batch-edit',
            json=updates,
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 200)
        
        # Verify changes
        for update in updates:
            response = self.app.get(f'/cars/show?reg={update["reg"]}')
            data = json.loads(response.data)
            self.assertEqual(data["colour"], update["updates"]["colour"])
            self.assertEqual(data["dayRate"], update["updates"]["dayRate"])

    def test_10_bulk_add(self):
        """Test bulk adding vehicles"""
        response = self.app.post(
            '/cars/bulk-add',
            json=self.bulk_vehicles,
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        
        # Verify response structure
        self.assertIn('added_count', data)
        self.assertIn('results', data)
        self.assertEqual(data['added_count'], len(self.bulk_vehicles))
        
        # Verify results for each vehicle
        for i, result in enumerate(data['results']):
            self.assertIn('vrm', result)
            self.assertIn('status', result)
            self.assertEqual(result['status'], 'success')
            
        # Verify all vehicles were added
        for vehicle in self.bulk_vehicles:
            response = self.app.get(f'/cars/show?reg={vehicle["vrm"]}')
            self.assertEqual(response.status_code, 200)
            data = json.loads(response.data)
            self.assertEqual(data["vrm"], vehicle["vrm"])

    def test_11_analytics(self):
        """Test analytics endpoints"""
        # Test fleet analytics
        response = self.app.get('/analytics/fleet')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertIn('summary', data)
        self.assertIn('fleet_composition', data)
        
        # Test branch analytics
        response = self.app.get('/analytics/branch?name=London')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertIn('branch_name', data)
        self.assertIn('total_vehicles', data)
        self.assertIn('available_vehicles', data)
        self.assertIn('rented_vehicles', data)
        self.assertIn('utilization_rate', data)
        self.assertIn('average_day_rate', data)
        self.assertIn('category_distribution', data)
        
        # Test rental analytics
        response = self.app.get('/analytics/rentals')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertIn('current_rentals', data)

    def test_12_account_management(self):
        """Test account management endpoints - Placeholder for future auth implementation"""
        pass

if __name__ == '__main__':
    unittest.main()
