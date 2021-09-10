from datetime import datetime
from http import HTTPStatus
from flask_restx import abort
from .models import Ride


def get_all_rides():
    """Fetches all rides
    and orders them by time they were created
    """

    rides = Ride.query.order_by(Ride.created_at).all()
    return rides


def create_ride(owner, ride_details):
    """Create a new ride and saves it
    """
    ride = Ride(owner, **ride_details)
    ride.save()
    return ride.id


def get_ride_by_id(id):
    """Fetch a ride by its id
    """
    return Ride.query.get(id)


def update_ride(ride_id, **ride_details):
    """Update a ride details
    """
    # TODO: make sure ride has not happened 
    ride = get_ride_by_id(ride_id)
    ride.vehicle_plate = ride_details['vehicle_plate']
    ride.seats = ride_details['seats']
    ride.town_from = ride_details['town_from']
    ride.town_to = ride_details['town_to']
    ride.depart_time = ride_details['depart_time']
    ride.end_time = ride_details['end_time']
    ride.created_at = datetime.utcnow()
    ride.save()


############################### Helper Methods ####################################
def check_active_ride(owner, depart_time):
    """Fetches an active ride
    Checks if a user has an active 
    ride that ends before the specified time
    
    Logic:
    If the depart time of ride to be created is 
    before(less than) the endtime of another ride by the same owner, then 
    the owner has an active ride
    
    Args:
        owner (Integer): id to search in the created_by column
        ttime (DateTime): time to compare with values in the endtime
    """
    for ride  in Ride.query.filter_by(created_by=owner):
        if ride.end_time > depart_time:
            return True
    return None


def abort_ride_has_departed_or_done(rideID):
    """Abort if ride has happened
    """
    ride = get_ride_by_id(rideID)
    time_now = datetime.utcnow()
    if ride.depart_time<=time_now or ride.end_time <= time_now:
        msg = "You Action is Prohibited: ride has departed/done"
        abort(HTTPStatus.FORBIDDEN, message=msg)


def abort_ride_not_found(rideID):
    """Abort if a ride does not exists
    """
    ride = get_ride_by_id(rideID)
    msg = 'Ride does not exist'
    if not ride:
        abort(HTTPStatus.NOT_FOUND, message=msg)


def abort_not_ride_owner(rideID, user):
    """Abort if user not same as that 
    of the ride
    """
    ride = get_ride_by_id(rideID)
    if ride.user_id != user:
        msg = 'Your are not authorized to view requests'
        abort(HTTPStatus.UNAUTHORIZED, message=msg)


def abort_ride_owner(rideID, user):
    """Abort if user making a request 
    to his own ride
    """
    ride = get_ride_by_id(rideID)
    if ride.user_id == user:
        msg = 'Prohibited to join your own ride'
        abort(HTTPStatus.BAD_REQUEST, message=msg)
