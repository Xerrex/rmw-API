from datetime import datetime
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
    ride = get_ride_by_id(ride_id)
    ride.vehicle_plate = ride_details['vehicle_plate']
    ride.seats = ride_details['seats']
    ride.town_from = ride_details['town_from']
    ride.town_to = ride_details['town_to']
    ride.depart_time = ride_details['depart_time']
    ride.end_time = ride_details['end_time']
    ride.created_at = datetime.utcnow()
    ride.save()



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

