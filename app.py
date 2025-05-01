from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import urllib.parse

db = SQLAlchemy()

def create_app(test_config=None):
    app = Flask(__name__)

    if test_config:
        app.config.update(test_config)
    else:
        username = "root"  # Replace with your MySQL username
        password = urllib.parse.quote_plus("mysql")  # Replace with your MySQL password
        host = "localhost"
        port = 3306  # Default port for MySQL
        database_name = "parking_system"  # Replace with your MySQL database name

        # Set the SQLAlchemy database URI for MySQL
        app.config['SQLALCHEMY_DATABASE_URI'] = f"mysql://{username}:{password}@{host}:{port}/{database_name}"
        app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.init_app(app)

    # Models
    class ParkingLot(db.Model):
        __tablename__ = 'parkinglots_details'  # Corrected table name
        parking_id = db.Column(db.Integer, primary_key=True)
        parking_name = db.Column(db.String(255))
        city = db.Column(db.String(100))
        parking_location = db.Column(db.String(255))
        address_1 = db.Column(db.String(255))
        address_2 = db.Column(db.String(255))
        latitude = db.Column(db.Float)
        longitude = db.Column(db.Float)
        physical_appearance = db.Column(db.String(255))
        parking_ownership = db.Column(db.String(100))
        parking_surface = db.Column(db.String(50))
        has_cctv = db.Column(db.String(10))
        has_boom_barrier = db.Column(db.String(10))
        ticket_generated = db.Column(db.String(50))
        entry_exit_gates = db.Column(db.Text)
        weekly_off = db.Column(db.String(50))
        parking_timing = db.Column(db.String(50))
        vehicle_types = db.Column(db.String(255))
        car_capacity = db.Column(db.Integer)
        two_wheeler_capacity = db.Column(db.Integer)
        parking_type = db.Column(db.String(50))
        payment_modes = db.Column(db.String(255))
        car_parking_charge = db.Column(db.String(50))
        two_wheeler_parking_charge = db.Column(db.String(50))
        allows_prepaid_passes = db.Column(db.String(10))
        provides_valet_services = db.Column(db.String(10))
        notes = db.Column(db.Text)
        total_slots = db.Column(db.Integer)
        available_slots = db.Column(db.Integer)

    class Floor(db.Model):
        __tablename__ = 'floors'
        floor_id = db.Column(db.Integer, primary_key=True)
        parking_id = db.Column(db.Integer, db.ForeignKey('parkinglots_details.parking_id'))
        floor_number = db.Column(db.String(50))
        total_slots = db.Column(db.Integer)
        available_slots = db.Column(db.Integer)

    class Row(db.Model):
        __tablename__ = 'parking_rows'
        row_id = db.Column(db.Integer, primary_key=True)
        parking_id = db.Column(db.Integer)
        floor_id = db.Column(db.Integer, db.ForeignKey('floors.floor_id'))
        row_number = db.Column(db.String(50))

    class Slot(db.Model):
        __tablename__ = 'slots'
        slot_id = db.Column(db.Integer, primary_key=True)
        parking_id = db.Column(db.Integer)
        row_id = db.Column(db.Integer, db.ForeignKey('parking_rows.row_id'))
        slot_number = db.Column(db.String(50))
        is_available = db.Column(db.Boolean, default=True)

    class ParkingSession(db.Model):
        __tablename__ = 'parkingsessions'
        session_id = db.Column(db.Integer, primary_key=True)
        user_id = db.Column(db.Integer)
        parking_id = db.Column(db.Integer)
        slot_id = db.Column(db.Integer, db.ForeignKey('slots.slot_id'))
        entry_time = db.Column(db.DateTime, default=datetime.utcnow)
        exit_time = db.Column(db.DateTime)
        car_number = db.Column(db.String(20))
        payment_status = db.Column(db.String(50))

    class User(db.Model):
        __tablename__ = 'users'
        user_id = db.Column(db.Integer, primary_key=True)
        username = db.Column(db.String(100), unique=True)
        password = db.Column(db.String(255))
        email = db.Column(db.String(100), unique=True)
        phone = db.Column(db.String(15))
        created_at = db.Column(db.DateTime, default=datetime.utcnow)

    # API Endpoints
    
    @app.route('/')
    def welcome():
        return """
    <h1>Welcome to Parking System</h1>
    <p>These are the available GET URLs for you to use:</p>
    <ul>
        <li><a href="/parkinglots/">GET /parkinglots/</a> - List all parking lots</li>
        <li><a href="/floors/1">GET /floors/&lt;parking_id&gt;</a> - List floors for a specific parking lot (Example for parking_id = 1)</li>
        <li><a href="/floors/">GET /floors/</a> - Get a list of all floors</li>
        <li><a href="/rows/1">GET /rows/&lt;floor_id&gt;</a> - List rows in a specific floor (Example for floor_id = 1)</li>
        <li><a href="/rows/">GET /rows/</a> - Get a list of all rows</li>
        <li><a href="/slots/1">GET /slots/&lt;row_id&gt;</a> - List available slots in a specific row (Example for row_id = 1)</li>
        <li><a href="/slots/">GET /slots/</a> - Get a list of all slots</li>
        <li><a href="/users/">GET /users/</a> - Get a list of all users</li>
        <li><a href="/users/5">GET /users/&lt;user_id&gt;</a> - Get details of a specific user (Example for user_id = 5)</li>
        <li><a href="/sessions/">GET /sessions/</a> - Get a list of all parking sessions</li>
    </ul>
    <p>To interact with POST or PUT endpoints, use <strong>Postman</strong> or <strong>curl</strong>.</p>
    <p>Here are the available POST and PUT endpoints:</p>
    <ul>
        <li><strong>POST /parkinglots/</strong> - Create a new parking lot</li>
        <li><strong>POST /floors/</strong> - Create a new floor in a parking lot</li>
        <li><strong>POST /rows/</strong> - Create a new row in a floor</li>
        <li><strong>POST /slots/</strong> - Create a new slot in a row</li>
        <li><strong>POST /Park_car/</strong> - Book a parking slot</li>
        <li><strong>PUT /Remove_car/&lt;session_id&gt;/exit</strong> - Release a booked parking slot</li>
    </ul>
    
    """


    # List Parking Lots
    @app.route('/parkinglots/', methods=['GET'])
    def list_parking_lots():
        parking_lots = ParkingLot.query.all()
        result = []
        for lot in parking_lots:
            result.append({
                'parking_id': lot.parking_id,
                'parking_name': lot.parking_name,
                'city': lot.city,
                'available_slots': lot.available_slots
            })
        return jsonify(result)

    # Create Parking Lot
    @app.route('/parkinglots/', methods=['POST'])
    def create_parking_lot():
        data = request.get_json()
        new_lot = ParkingLot(
            parking_name=data['parking_name'],
            city=data['city'],
            parking_location=data['parking_location'],
            address_1=data['address_1'],
            address_2=data['address_2'],
            latitude=data['latitude'],
            longitude=data['longitude'],
            physical_appearance=data['physical_appearance'],
            parking_ownership=data['parking_ownership'],
            parking_surface=data['parking_surface'],
            has_cctv=data['has_cctv'],
            has_boom_barrier=data['has_boom_barrier'],
            ticket_generated=data['ticket_generated'],
            entry_exit_gates=data['entry_exit_gates'],
            weekly_off=data['weekly_off'],
            parking_timing=data['parking_timing'],
            vehicle_types=data['vehicle_types'],
            car_capacity=data['car_capacity'],
            two_wheeler_capacity=data['two_wheeler_capacity'],
            parking_type=data['parking_type'],
            payment_modes=data['payment_modes'],
            car_parking_charge=data['car_parking_charge'],
            two_wheeler_parking_charge=data['two_wheeler_parking_charge'],
            allows_prepaid_passes=data['allows_prepaid_passes'],
            provides_valet_services=data['provides_valet_services'],
            notes=data['notes'],
            total_slots=data['total_slots'],
            available_slots=data['available_slots']
        )
        db.session.add(new_lot)
        db.session.commit()
        return jsonify({'message': 'Parking lot created successfully', 'parking_id': new_lot.parking_id}), 201
    
    #ALL FLOORS
    @app.route('/floors/', methods=['GET'])
    def list_all_floors():
        floors = Floor.query.all()
        result = [{
        'floor_id': floor.floor_id,
        'floor_number': floor.floor_number,
        'total_slots': floor.total_slots,
        'available_slots': floor.available_slots,
        'parking_id': floor.parking_id  # Include parking_id for context
        } for floor in floors]
        return jsonify(result), 200


    # List Floors of a Parking Lot
    @app.route('/floors/<int:parking_id>', methods=['GET'])
    def list_floors(parking_id):
        floors = Floor.query.filter_by(parking_id=parking_id).all()
        result = []
        for floor in floors:
            result.append({
                'floor_id': floor.floor_id,
                'floor_number': floor.floor_number,
                'total_slots': floor.total_slots,
                'available_slots': floor.available_slots
            })
        return jsonify(result)

    # Create Floor
    @app.route('/floors/', methods=['POST'])
    def create_floor():
        data = request.get_json()
        new_floor = Floor(
            parking_id=data['parking_id'],
            floor_number=data['floor_number'],
            total_slots=data['total_slots'],
            available_slots=data['available_slots']
        )
        db.session.add(new_floor)
        db.session.commit()
        return jsonify({'message': 'Floor created successfully', 'floor_id': new_floor.floor_id}), 201
    
    #AllRows
    @app.route('/rows/', methods=['GET'])
    def list_all_rows():
        rows = Row.query.all()
        result = [{
        'row_id': row.row_id,
        'row_number': row.row_number,
        'floor_id': row.floor_id
        } for row in rows]
        return jsonify(result), 200


    # List Rows in a Floor
    @app.route('/rows/<int:floor_id>', methods=['GET'])
    def list_rows(floor_id):
        rows = Row.query.filter_by(floor_id=floor_id).all()
        result = []
        for row in rows:
            result.append({
                'row_id': row.row_id,
                'row_number': row.row_number
            })
        return jsonify(result)

    # Create Row
    @app.route('/rows/', methods=['POST'])
    def create_row():
        data = request.get_json()
        new_row = Row(
            parking_id=data['parking_id'],
            floor_id=data['floor_id'],
            row_number=data['row_number']
        )
        db.session.add(new_row)
        db.session.commit()
        return jsonify({'message': 'Row created successfully', 'row_id': new_row.row_id}), 201
    
    #All slots
    @app.route('/slots/', methods=['GET'])
    def list_all_slots():
        slots = Slot.query.all()
        result = [{
        'slot_id': slot.slot_id,
        'slot_number': slot.slot_number,
        'row_id': slot.row_id,
        'is_available': slot.is_available
        } for slot in slots]
        return jsonify(result), 200


    # List Available Slots in a Row
    @app.route('/slots/<int:row_id>', methods=['GET'])
    def list_slots(row_id):
        slots = Slot.query.filter_by(row_id=row_id, is_available=True).all()
        result = []
        for slot in slots:
            result.append({
                'slot_id': slot.slot_id,
                'slot_number': slot.slot_number
            })
        return jsonify(result)

    # Create Slot
    @app.route('/slots/', methods=['POST'])
    def create_slot():
        data = request.get_json()
        new_slot = Slot(
            parking_id=data['parking_id'],
            row_id=data['row_id'],
            slot_number=data['slot_number']
        )
        db.session.add(new_slot)
        db.session.commit()
        return jsonify({'message': 'Slot created successfully', 'slot_id': new_slot.slot_id}), 201
    
    
    #All sessions details 
    @app.route('/sessions/', methods=['GET'])
    def get_all_sessions():
        sessions = ParkingSession.query.all()
        session_list = []
        for session in sessions:
            session_data = {
            'session_id': session.session_id,
            'user_id': session.user_id,
            'parking_id': session.parking_id,
            'slot_id': session.slot_id,
            'car_number': session.car_number,
            'entry_time': session.entry_time.strftime('%a, %d %b %Y %H:%M:%S GMT'),
            'exit_time': session.exit_time.strftime('%a, %d %b %Y %H:%M:%S GMT') if session.exit_time else None
            }
            session_list.append(session_data)
        return jsonify({'sessions': session_list}), 200


    # Book a Parking Slot
    @app.route('/Park_car/', methods=['POST'])
    def book_parking_slot():
        data = request.get_json()
        slot = Slot.query.get(data['slot_id'])
        if slot and slot.is_available:
            slot.is_available = False
            session = ParkingSession(
                user_id=data['user_id'],
                parking_id=data['parking_id'],
                slot_id=data['slot_id'],
                car_number=data['car_number']
            )
            db.session.add(session)
            db.session.commit()
            return jsonify({'message': 'Parking slot booked successfully', 'session_id': session.session_id}), 201
        else:
            return jsonify({'message': 'Slot is unavailable'}), 400

    # Release a Parking Slot
    @app.route('/Remove_car/<int:session_id>/exit', methods=['PUT'])
    def release_parking_slot(session_id):
        session = ParkingSession.query.get(session_id)
        if session:
            slot = Slot.query.get(session.slot_id)
            slot.is_available = True
            session.exit_time = datetime.utcnow()
            db.session.commit()
            return jsonify({'message': 'Parking slot released successfully'}), 200
        else:
            return jsonify({'message': 'Session not found'}), 404

    # User Registration
    @app.route('/users/register', methods=['POST'])
    def register_user():
        data = request.get_json()
        new_user = User(
            username=data['username'],
            password=data['password'],
            email=data['email'],
            phone=data['phone']
        )
        db.session.add(new_user)
        db.session.commit()
        return jsonify({'message': 'User registered successfully', 'user_id': new_user.user_id}), 201

    # User Login
    @app.route('/users/login', methods=['POST'])
    def login_user():
        data = request.get_json()
        user = User.query.filter_by(email=data['email']).first()
        if user and user.password == data['password']:
            return jsonify({'message': 'Login successful', 'user_id': user.user_id}), 200
        else:
            return jsonify({'message': 'Invalid credentials'}), 400
    
    #GET particular USER details relace user_id on your choice 
    @app.route('/users/<int:user_id>', methods=['GET'])
    def get_user(user_id):
        user = User.query.get(user_id)
        if user:
            user_data = {
            'user_id': user.user_id,
            'username': user.username,
            'email': user.email,
            'phone': user.phone,
            'created_at': user.created_at.strftime('%a, %d %b %Y %H:%M:%S GMT')
            }
            return jsonify(user_data), 200
        else:
            return jsonify({'message': 'User not found'}), 404

        
    # Get all User Details
    @app.route('/users/', methods=['GET'])
    def get_all_users():
        users = User.query.all()  # Get all users from the database
        user_list = []
        for user in users:
            user_data = {
                'user_id': user.user_id,
            'username': user.username,
            'email': user.email,
            'phone': user.phone,
            'created_at': user.created_at.strftime('%a, %d %b %Y %H:%M:%S GMT')  # Formatting the created_at field
            }
            user_list.append(user_data)
        return jsonify({'users': user_list}), 200


    '''
    # this helps to create table schema in database - no need to do manually
    with app.app_context():
        db.create_all()
        
        #to create the database tables automatically
        #you must create the database manually first before db.create_all() can create the tables inside it.
    '''

    return app
