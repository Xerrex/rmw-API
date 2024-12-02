from .db_setup import Base


class User(Base):
    """User
    """

    # id = db.Column(db.Integer, primary_key=True)
    # name = db.Column(db.String(255), nullable=False)
    # username = db.Column(db.String(120), unique=True, nullable=False)
    # email = db.Column(db.String(255), unique=True, nullable=False)
    # password = db.Column(db.String(255), nullable=False)
    # last_login = db.Column(db.DateTime, default=datetime.utcnow)
    # created_at
    # updated_at
    # rides = db.relationship('Ride', backref='owner', lazy=True)
    # ride_requests = db.relationship('RideRequest', backref='passenger', lazy=True)


    # TODO: Token generation and verification
    pass


class Ride(Base):
    """Ride
    """
    # id = db.Column(db.Integer, primary_key=True)
    # vehicle_plate = db.Column(db.String(15), nullable=False)
    # seats = db.Column(db.Integer, nullable=False)
    # town_from = db.Column(db.String(80), nullable=False)
    # town_to = db.Column(db.String(80), nullable=False)
    # depart_time = db.Column(db.DateTime, nullable=False)
    # end_time = db.Column(db.DateTime, nullable=False)
    # created_at = db.Column(db.DateTime, default=datetime.utcnow)
    # updated_at 
    # created_by = db.Column(db.Integer, db.ForeignKey('user.id'),nullable=False)
    # ride_requests = db.relationship('RideRequest', backref='ride', lazy=True)
    pass


class RideRequest(Base):
    """Ride Request 
    """

    # id = db.Column(db.Integer,primary_key=True)
    # ride_id = db.Column(db.Integer, db.ForeignKey('ride.id'), nullable='False')
    # user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable='False')
    # seats = db.Column(db.Integer, nullable=False, default=1)
    # stop = db. Column(db.String(25), default='Ride Destination', nullable=False)
    # status = db.Column(db.String(9), nullable='False', default='Pending') # Accepted/Rejected
    # created_at = db.Column(db.DateTime, default=datetime.utcnow)
    # updated_at 
    pass
