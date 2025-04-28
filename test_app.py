import pytest
from app import create_app, db
from flask_testing import TestCase
from datetime import datetime


class TestParkingApp(TestCase):

    def create_app(self):
        return create_app(test_config={'TESTING': True, 'SQLALCHEMY_DATABASE_URI': 'sqlite:///:memory:'})

    def setUp(self):
        self.client = self.app.test_client()
        db.create_all()  # Create all tables

    def tearDown(self):
        db.session.remove()
        db.drop_all()

    def test_welcome(self):
        """Test the / endpoint to ensure it returns the welcome message"""
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"Welcome to Parking System", response.data)

    def test_list_parking_lots(self):
        """Test the /parkinglots/ endpoint to list parking lots"""
        response = self.client.get('/parkinglots/')
        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(response.json, list)

    def test_create_parking_lot(self):
        """Test the POST /parkinglots/ endpoint to create a new parking lot"""
        data = {
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
        response = self.client.post('/parkinglots/', json=data)
        self.assertEqual(response.status_code, 201)
        self.assertIn('Parking lot created successfully', response.json['message'])

    def test_list_floors(self):
        """Test the /floors/&lt;parking_id&gt; endpoint to list floors for a parking lot"""
        # Create a parking lot first
        parking_lot_data = {
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
        parking_lot_response = self.client.post('/parkinglots/', json=parking_lot_data)
        parking_id = parking_lot_response.json['parking_id']

        # Now create a floor
        floor_data = {
            'parking_id': parking_id,
            'floor_number': '1',
            'total_slots': 50,
            'available_slots': 50
        }
        self.client.post('/floors/', json=floor_data)

        # Test listing floors
        response = self.client.get(f'/floors/{parking_id}')
        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(response.json, list)

    def test_create_floor(self):
        """Test the POST /floors/ endpoint to create a new floor"""
        # Create a parking lot first
        parking_lot_data = {
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
        parking_lot_response = self.client.post('/parkinglots/', json=parking_lot_data)
        parking_id = parking_lot_response.json['parking_id']

        # Create floor
        floor_data = {
            'parking_id': parking_id,
            'floor_number': '1',
            'total_slots': 50,
            'available_slots': 50
        }
        response = self.client.post('/floors/', json=floor_data)
        self.assertEqual(response.status_code, 201)
        self.assertIn('Floor created successfully', response.json['message'])

    def test_list_rows(self):
        """Test the /rows/&lt;floor_id&gt; endpoint to list rows in a floor"""
        # Create a parking lot and floor first
        parking_lot_data = {
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
        parking_lot_response = self.client.post('/parkinglots/', json=parking_lot_data)
        parking_id = parking_lot_response.json['parking_id']

        floor_data = {
            'parking_id': parking_id,
            'floor_number': '1',
            'total_slots': 50,
            'available_slots': 50
        }
        floor_response = self.client.post('/floors/', json=floor_data)
        floor_id = floor_response.json['floor_id']

        # Create rows
        row_data = {'parking_id': parking_id, 'floor_id': floor_id, 'row_number': 'A'}
        self.client.post('/rows/', json=row_data)

        # Test listing rows
        response = self.client.get(f'/rows/{floor_id}')
        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(response.json, list)

    def test_create_row(self):
        """Test the POST /rows/ endpoint to create a new row"""
        # Create parking lot, floor first
        parking_lot_data = {
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
        parking_lot_response = self.client.post('/parkinglots/', json=parking_lot_data)
        parking_id = parking_lot_response.json['parking_id']

        floor_data = {
            'parking_id': parking_id,
            'floor_number': '1',
            'total_slots': 50,
            'available_slots': 50
        }
        floor_response = self.client.post('/floors/', json=floor_data)
        floor_id = floor_response.json['floor_id']

        # Create a row
        row_data = {'parking_id': parking_id, 'floor_id': floor_id, 'row_number': 'A'}
        response = self.client.post('/rows/', json=row_data)
        self.assertEqual(response.status_code, 201)
        self.assertIn('Row created successfully', response.json['message'])

    def test_list_slots(self):
        """Test the /slots/&lt;row_id&gt; endpoint to list slots in a row"""
        # Create parking lot, floor, and row first
        parking_lot_data = {
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
        parking_lot_response = self.client.post('/parkinglots/', json=parking_lot_data)
        parking_id = parking_lot_response.json['parking_id']

        floor_data = {
            'parking_id': parking_id,
            'floor_number': '1',
            'total_slots': 50,
            'available_slots': 50
        }
        floor_response = self.client.post('/floors/', json=floor_data)
        floor_id = floor_response.json['floor_id']

        row_data = {'parking_id': parking_id, 'floor_id': floor_id, 'row_number': 'A'}
        row_response = self.client.post('/rows/', json=row_data)
        row_id = row_response.json['row_id']

        # Create slots
        slot_data = {'parking_id': parking_id, 'row_id': row_id, 'slot_number': '1'}
        self.client.post('/slots/', json=slot_data)

        # Test listing slots
        response = self.client.get(f'/slots/{row_id}')
        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(response.json, list)

    def test_create_slot(self):
        """Test the POST /slots/ endpoint to create a new slot"""
        # Create parking lot, floor, and row first
        parking_lot_data = {
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
        parking_lot_response = self.client.post('/parkinglots/', json=parking_lot_data)
        parking_id = parking_lot_response.json['parking_id']

        floor_data = {
            'parking_id': parking_id,
            'floor_number': '1',
            'total_slots': 50,
            'available_slots': 50
        }
        floor_response = self.client.post('/floors/', json=floor_data)
        floor_id = floor_response.json['floor_id']

        row_data = {'parking_id': parking_id, 'floor_id': floor_id, 'row_number': 'A'}
        row_response = self.client.post('/rows/', json=row_data)
        row_id = row_response.json['row_id']

        # Create a slot
        slot_data = {'parking_id': parking_id, 'row_id': row_id, 'slot_number': '1'}
        response = self.client.post('/slots/', json=slot_data)
        self.assertEqual(response.status_code, 201)
        self.assertIn('Slot created successfully', response.json['message'])

    def test_create_user(self):
        """Test creating a user"""
        user_data = {
            'name': 'Test User',
            'email': 'testuser@example.com',
            'phone': '1234567890',
            'license_plate': 'ABCD1234',
            'vehicle_type': 'Car'
        }
        response = self.client.post('/users/', json=user_data)
        self.assertEqual(response.status_code, 201)
        self.assertIn('User created successfully', response.json['message'])

    def test_create_parking_session(self):
        """Test creating a parking session"""
        # Create user and parking lot
        user_data = {
            'name': 'Test User',
            'email': 'testuser@example.com',
            'phone': '1234567890',
            'license_plate': 'ABCD1234',
            'vehicle_type': 'Car'
        }
        user_response = self.client.post('/users/', json=user_data)
        user_id = user_response.json['user_id']

        parking_lot_data = {
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
        parking_lot_response = self.client.post('/parkinglots/', json=parking_lot_data)
        parking_id = parking_lot_response.json['parking_id']

        floor_data = {
            'parking_id': parking_id,
            'floor_number': '1',
            'total_slots': 50,
            'available_slots': 50
        }
        floor_response = self.client.post('/floors/', json=floor_data)
        floor_id = floor_response.json['floor_id']

        row_data = {'parking_id': parking_id, 'floor_id': floor_id, 'row_number': 'A'}
        row_response = self.client.post('/rows/', json=row_data)
        row_id = row_response.json['row_id']

        slot_data = {'parking_id': parking_id, 'row_id': row_id, 'slot_number': '1'}
        slot_response = self.client.post('/slots/', json=slot_data)
        slot_id = slot_response.json['slot_id']

        session_data = {
            'user_id': user_id,
            'slot_id': slot_id,
            'start_time': str(datetime.now()),
            'end_time': None,
            'charge': 10
        }

        response = self.client.post('/sessions/', json=session_data)
        self.assertEqual(response.status_code, 201)
        self.assertIn('Parking session created successfully', response.json['message'])

if __name__ == '__main__':
    pytest.main()
