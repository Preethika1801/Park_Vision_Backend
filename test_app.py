import pytest
from app import create_app
from flask_testing import TestCase

class TestParkingApp(TestCase):
    
    def create_app(self):
        # Configure the app for testing by using an in-memory SQLite database
        return create_app(test_config={'TESTING': True, 'SQLALCHEMY_DATABASE_URI': 'sqlite:///:memory:'})

    def setUp(self):
        # Set up any state before running tests
        self.client = self.app.test_client()  # Use Flask's test client for sending HTTP requests

    def test_welcome(self):
        """Test the / endpoint to ensure it returns the welcome message"""
        response = self.client.get('/')  # Send a GET request to the root endpoint
        self.assertEqual(response.status_code, 200)  # Check if the response status code is 200 (OK)
        self.assertIn(b"Welcome to Parking System", response.data)  # Ensure the welcome message is in the response

    def test_list_parking_lots(self):
        """Test the /parkinglots/ endpoint to list parking lots"""
        response = self.client.get('/parkinglots/')  # Send a GET request to the parkinglots endpoint
        self.assertEqual(response.status_code, 200)  # Ensure the status code is 200 (OK)
        self.assertIsInstance(response.json, list)  # Check that the response is a list of parking lots

    def test_create_parking_lot(self):
        """Test the POST /parkinglots/ endpoint to create a new parking lot"""
        data = {  # Data for the new parking lot
            'parking_name': 'Test Lot',
            'city': 'Test City',
            'parking_location': 'Test Location',
            'address_1': '123 Test St',
            'address_2': 'Suite 101',
            'latitude': 12.3456,
            'longitude': 78.9012,
            'physical_appearance': 'Good',
            'parking_ownership': 'Private',
            'parking_surface': 'Paved',
            'has_cctv': 'Yes',
            'has_boom_barrier': 'Yes',
            'ticket_generated': 'Yes',
            'entry_exit_gates': '1',
            'weekly_off': 'Sunday',
            'parking_timing': '24/7',
            'vehicle_types': 'Car',
            'car_capacity': 50,
            'two_wheeler_capacity': 20,
            'parking_type': 'Covered',
            'payment_modes': 'Cash, Card',
            'car_parking_charge': '10',
            'two_wheeler_parking_charge': '5',
            'allows_prepaid_passes': 'Yes',
            'provides_valet_services': 'No',
            'notes': 'N/A',
            'total_slots': 100,
            'available_slots': 50
        }
        response = self.client.post('/parkinglots/', json=data)  # Send a POST request to create the parking lot
        self.assertEqual(response.status_code, 201)  # Ensure the status code is 201 (Created)
        self.assertIn('Parking lot created successfully', response.json['message'])  # Check the success message

if __name__ == '__main__':
    pytest.main()  # Run pytest when the file is executed directly
