from .models import RideRequest


def get_ride_requests(rideID):
    """Fetch all requests
    """
    reqs = RideRequest.query.filter(RideRequest.ride_id==rideID).all()
    return reqs
