from app.data.models import User
from app.data.models import Ride
from app.data.models import RideRequest


# 2021-08-04 05:35:08.817837 datetime.utcnow()
DT_FORMAT = '%Y-%m-%d %H:%M:%S.%f' 


def create_user(name, username, email,password):
    """Create a new User instance
    """
    return User(name, username, email, password)


def create_ride(owner, ride_data):
    """Create a new Ride instance
    """

    return Ride(owner, **ride_data)


def create_ride_request(ride, passenger, stop, seats):
    """Create a new RideRequest instance
    """
    return RideRequest(ride, passenger, stop, seats)