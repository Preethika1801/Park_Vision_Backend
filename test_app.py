import pytest
from app import create_app, db

@pytest.fixture(scope="session")
def app():
    app = create_app({
        'TESTING': True,
        'SQLALCHEMY_DATABASE_URI': 'sqlite:///:memory:',
        'SQLALCHEMY_TRACK_MODIFICATIONS': False
    })

    with app.app_context():
        db.reflect()        # Drop previously defined tables to avoid metadata conflict
        db.drop_all()
        db.create_all()

    return app

@pytest.fixture
def client(app):
    return app.test_client()

def test_welcome_page(client):
    response = client.get('/')
    assert response.status_code == 200
    assert b"Welcome to Parking System" in response.data

def test_user_registration_and_login(client):
    # Register a new user
    user_data = {
        'username': 'testuser',
        'password': 'testpass',
        'email': 'test@example.com',
        'phone': '1234567890'
    }
    response = client.post('/users/register', json=user_data)
    assert response.status_code == 201
    user_id = response.get_json()['user_id']

    # Attempt login with correct credentials
    login_data = {
        'email': 'test@example.com',
        'password': 'testpass'
    }
    response = client.post('/users/login', json=login_data)
    assert response.status_code == 200
    assert response.get_json()['user_id'] == user_id

def test_parking_lot_creation_and_listing(client):
    # Create a new parking lot
    parking_lot_data = {
        'parking_name': 'Central Park',
        'city': 'Metropolis',
        'parking_location': 'Downtown',
        'address_1': '123 Main St',
        'address_2': 'Suite 100',
        'latitude': 40.7128,
        'longitude': -74.0060,
        'physical_appearance': 'Multi-level',
        'parking_ownership': 'Public',
        'parking_surface': 'Concrete',
        'has_cctv': 'Yes',
        'has_boom_barrier': 'Yes',
        'ticket_generated': 'Digital',
        'entry_exit_gates': 'North Gate, South Gate',
        'weekly_off': 'Sunday',
        'parking_timing': '24/7',
        'vehicle_types': 'Car, Bike',
        'car_capacity': 100,
        'two_wheeler_capacity': 50,
        'parking_type': 'Multi-level',
        'payment_modes': 'Cash, Card',
        'car_parking_charge': '20',
        'two_wheeler_parking_charge': '10',
        'allows_prepaid_passes': 'Yes',
        'provides_valet_services': 'No',
        'notes': 'Open during holidays',
        'total_slots': 150,
        'available_slots': 150
    }
    response = client.post('/parkinglots/', json=parking_lot_data)
    assert response.status_code == 201
    parking_id = response.get_json()['parking_id']

    # List all parking lots
    response = client.get('/parkinglots/')
    assert response.status_code == 200
    data = response.get_json()
    assert any(lot['parking_id'] == parking_id for lot in data)

def test_floor_creation_and_listing(client):
    # First, create a parking lot
    parking_lot_data = {
        'parking_name': 'Central Park',
        'city': 'Metropolis',
        'parking_location': 'Downtown',
        'address_1': '123 Main St',
        'address_2': 'Suite 100',
        'latitude': 40.7128,
        'longitude': -74.0060,
        'physical_appearance': 'Multi-level',
        'parking_ownership': 'Public',
        'parking_surface': 'Concrete',
        'has_cctv': 'Yes',
        'has_boom_barrier': 'Yes',
        'ticket_generated': 'Digital',
        'entry_exit_gates': 'North Gate, South Gate',
        'weekly_off': 'Sunday',
        'parking_timing': '24/7',
        'vehicle_types': 'Car, Bike',
        'car_capacity': 100,
        'two_wheeler_capacity': 50,
        'parking_type': 'Multi-level',
        'payment_modes': 'Cash, Card',
        'car_parking_charge': '20',
        'two_wheeler_parking_charge': '10',
        'allows_prepaid_passes': 'Yes',
        'provides_valet_services': 'No',
        'notes': 'Open during holidays',
        'total_slots': 150,
        'available_slots': 150
    }
    response = client.post('/parkinglots/', json=parking_lot_data)
    parking_id = response.get_json()['parking_id']

    # Create a floor
    floor_data = {
        'parking_id': parking_id,
        'floor_number': '1',
        'total_slots': 50,
        'available_slots': 50
    }
    response = client.post('/floors/', json=floor_data)
    assert response.status_code == 201
    floor_id = response.get_json()['floor_id']

    # List floors for the parking lot
    response = client.get(f'/floors/{parking_id}')
    assert response.status_code == 200
    data = response.get_json()
    assert any(floor['floor_id'] == floor_id for floor in data)

def test_row_creation_and_listing(client):
    # Create parking lot
    parking_lot_data = {
        'parking_name': 'Central Park',
        'city': 'Metropolis',
        'parking_location': 'Downtown',
        'address_1': '123 Main St',
        'address_2': 'Suite 100',
        'latitude': 40.7128,
        'longitude': -74.0060,
        'physical_appearance': 'Multi-level',
        'parking_ownership': 'Public',
        'parking_surface': 'Concrete',
        'has_cctv': 'Yes',
        'has_boom_barrier': 'Yes',
        'ticket_generated': 'Digital',
        'entry_exit_gates': 'North Gate, South Gate',
        'weekly_off': 'Sunday',
        'parking_timing': '24/7',
        'vehicle_types': 'Car, Bike',
        'car_capacity': 100,
        'two_wheeler_capacity': 50,
        'parking_type': 'Multi-level',
        'payment_modes': 'Cash, Card',
        'car_parking_charge': '20',
        'two_wheeler_parking_charge': '10',
        'allows_prepaid_passes': 'Yes',
        'provides_valet_services': 'No',
        'notes': 'Open during holidays',
        'total_slots': 150,
        'available_slots': 150
    }
    response = client.post('/parkinglots/', json=parking_lot_data)
    parking_id = response.get_json()['parking_id']

    # Create floor
    floor_data = {
        'parking_id': parking_id,
        'floor_number': '1',
        'total_slots': 50,
        'available_slots': 50
    }
    response = client.post('/floors/', json=floor_data)
    floor_id = response.get_json()['floor_id']

    # Create a row
    row_data = {
        'parking_id': parking_id,
        'floor_id': floor_id,
        'row_number': 'A'
    }
    response = client.post('/rows/', json=row_data)
    assert response.status_code == 201
    row_id = response.get_json()['row_id']

    # List rows for the floor
    response = client.get(f'/rows/{floor_id}')
    assert response.status_code == 200
    data = response.get_json()
    assert any(row['row_id'] == row_id for row in data)

def test_slot_creation_and_listing(client):
    # Create parking lot
    parking_lot_data = {
        'parking_name': 'Central Park',
        'city': 'Metropolis',
        'parking_location': 'Downtown',
        'address_1': '123 Main St',
        'address_2': 'Suite 100',
        'latitude': 40.7128,
        'longitude': -74.0060,
        'physical_appearance': 'Multi-level',
        'parking_ownership': 'Public',
        'parking_surface': 'Concrete',
        'has_cctv': 'Yes',
        'has_boom_barrier': 'Yes',
        'ticket_generated': 'Digital',
        'entry_exit_gates': 'North Gate, South Gate',
        'weekly_off': 'Sunday',
        'parking_timing': '24/7',
        'vehicle_types': 'Car, Bike',
        'car_capacity': 100,
        'two_wheeler_capacity': 50,
        'parking_type': 'Multi-level',
        'payment_modes': 'Cash, Card',
        'car_parking_charge': '20',
        'two_wheeler_parking_charge': '10',
        'allows_prepaid_passes': 'Yes',
        'provides_valet_services': 'No',
        'notes': 'Open during holidays',
        'total_slots': 150,
        'available_slots': 150
    }
    response = client.post('/parkinglots/', json=parking_lot_data)
    parking_id = response.get_json()['parking_id']

    # Create floor
    floor_data = {
        'parking_id': parking_id,
        'floor_number': '1',
        'total_slots': 50,
        'available_slots': 50
    }
    response = client.post('/floors/', json=floor_data)
    floor_id = response.get_json()['floor_id']

    # Create row
    row_data = {
        'parking_id': parking_id,
        'floor_id': floor_id,
        'row_number': 'A'
    }
    response = client.post('/rows/', json=row_data)
    row_id = response.get_json()['row_id']

    # Create a slot
    slot_data = {
        'parking_id': parking_id,
        'row_id': row_id,
        'slot_number': '1'
    }
    response = client.post('/slots/', json=slot_data)
    assert response.status_code == 201
    slot_id = response.get_json()['slot_id']

    # List available slots for the row
    response = client.get(f'/slots/{row_id}')
    assert response.status_code == 200
    data = response.get_json()
    assert any(slot['slot_id'] == slot_id for slot in data)
 