from datetime import datetime
from sqlalchemy.orm import backref

from werkzeug.security import check_password_hash, \
    generate_password_hash

from flask_jwt_extended import create_access_token

from app.utils.exts import db

DT_FORMAT = '%Y-%m-%d %H:%M:%S.%f' # 2021-08-04 05:35:08.817837


class User(db.Model):
    """The User Model
    """
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    username = db.Column(db.String(120), unique=True, nullable=False)
    email = db.Column(db.String(255), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    last_login = db.Column(db.DateTime, default=datetime.utcnow)
    rides = db.relationship('Ride', backref='owner', lazy=True)
    my_requests = db.relationship('RideRequest', backref='passenger', lazy=True)

    def __init__(self, name, username, email, password):
        """Defines how to create a new User

        Args:
            name (String): name of the User
            username (String): a unique name to identify user
            email (String): an Email formated string
            password (String): The secret key to authenticate a user
        """

        self.name = name
        self.username = username # TODO: Remove fieldS
        self.email = email
        self.password = generate_password_hash(password)
    
    def save(self):
        """Method to save or update user details
        """
        db.session.add(self)
        db.session.commit()

    def __repr__(self) -> str:
        """Define how a User is printed
        """
        return f'User-{self.username}'
    
    def verify_password(self, password):
        """Verify the password of a user

        Args:
            password (String): The secret key to authenticate a user

        Returns:
            bool : True or False
        """
        
        return check_password_hash(self.password, password)
    
    def generate_access_token(self):
        """Create a JWT access token
        """
        identity = self.username
        access_token = create_access_token(identity=identity)
        return access_token


class Ride(db.Model):
    """Defines a Ride model

    It describes a situation where someone wants 
    to share passenger spaces in their ride.
    """

    id = db.Column(db.Integer, primary_key=True)
    vehicle_plate = db.Column(db.String(15), nullable=False)
    seats = db.Column(db.Integer, nullable=False)
    town_from = db.Column(db.String(80), nullable=False)
    town_to = db.Column(db.String(80), nullable=False)
    depart_time = db.Column(db.DateTime, nullable=False)
    end_time = db.Column(db.DateTime, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    created_by = db.Column(db.Integer, db.ForeignKey('user.id'),nullable=False)
    requests = db.relationship('RideRequest', backref='ride', lazy=True)

    def __init__(self, owner, **kwargs):
        """Defines how to create a ride

        Args:
            owner (Integer): ID of the creator of the ride
        KeyWord args:
            vehicle_plate (String): Vehicle Number plate eg. 'KCH 020'
            seats (Integer): Number of available passenger spaces eg. 1
            town_from (String): Town from which the ride starts
            town_to (String): Town to which the ride is headed to
            depart_time (DateTime String): Time which the ride leaves t_from
            end_time(DateTime String): Time which the ride reaches t_to
        """
        self.vehicle_plate = kwargs['vehicle_plate']
        self.seats = kwargs['seats']
        self.town_from = kwargs['town_from']
        self.town_to = kwargs['town_to']
        self.created_by = owner
        self.depart_time = kwargs['depart_time'] 
        self.end_time = kwargs['end_time']
        
    
    def save(self):
        "Save a ride"
        self.depart_time = datetime.strptime(self.depart_time, DT_FORMAT) # 2021-08-04 05:35:08.817837
        self.end_time = datetime.strptime(self.end_time, DT_FORMAT)
        db.session.add(self)
        db.session.commit()
    
    def __repr__(self) -> str:
        """Define how a ride is printed"""
        r_time = self.depart_time
        r_from = self.town_from
        r_to = self.town_to
        return f'Ride at {r_time}: {r_from} - {r_to}'


class RideRequest(db.Model):
    """Define a situation where a 
    User makes a request to join a ride
    """
    id = db.Column(db.Integer,primary_key=True)
    ride_id = db.Column(db.Integer, db.ForeignKey('ride.id'), nullable='False')
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable='False')
    seats = db.Column(db.Integer, nullable=False, default=1)
    stop = db. Column(db.String(25), default='Ride Destination', nullable=False)
    status = db.Column(db.String(9), nullable='False', default='Pending') # Accepted/Rejected
    made_at = db.Column(db.DateTime, nullable='False')

    def __init__(self, ride, passenger, stop=None, seats=1):
        """Define hou to create a request

        Args:
            ride (int): The ID of a ride
            passenger (str): The ID of a User
            stop (str): The destination a user is going
            seats (int, optional): The number of seats requesting. Defaults to 1.
        """
        self.ride_id = ride
        self.user_id = passenger
        self.stop = stop
        self.seats = seats
        self.made_at = datetime.utcnow()
    
    def save(self):
        """Create/update a Request
        request in the db
        """
        db.session.add(self)
        db.session.commit()
    
    def delete(self):
        """Delete a request
        """
        db.session.delete(self)
        db.session.commit()

    def __repr__(self):
        """Define how a RideRequest 
        is represented
        """
        return f'RideRequest-{self.made_at}-{self.stop}'
