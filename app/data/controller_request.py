from http import HTTPStatus
from flask_restx import abort
from .models import RideRequest


def get_ride_requests(rideID):
    """Fetch all requests
    """
    reqs = RideRequest.query.filter(RideRequest.ride_id==rideID).all()
    return reqs

def get_ride_request(reqID):
    """Fetch a single request
    """
    req = RideRequest.query.get(reqID)
    return req

def make_request(rideID, passenger, stop, seats):
    """Make a request 
    """
    req  = RideRequest(rideID, passenger, stop, seats)
    req.save()
    return req.id

def update_request(reqID, stop,seats):
    req = get_ride_request(reqID)
    req.stop = stop
    req.seats = seats
    req.save()

def delete_request(reqID):
    """Delete a Request
    """
    req = get_ride_request(reqID)
    req.delete()

def request_action(reqID, action):
    """Accept or Reject a Request
    """
    req = get_ride_request(reqID)
    req.status = action.lower().title()
    req.save();
    
        

###################### Helper Methods ##############################
def abort_already_made_request(rideID, user):
    """Abort if user has already made a request
    """
    reqs = get_ride_requests(rideID)

    for req in reqs:
        if req.user_id == user:
            msg = "You have already made a request"
            abort(HTTPStatus.CONFLICT, message=msg)


def abort_request_not_found(reqID):
    """Abort if request does not exists
    """
    req = get_ride_request(reqID)
    if not req:
        msg="The Request does not exist"
        abort(HTTPStatus.NOT_FOUND, message=msg)


def abort_request_already_accepted(reqID):
    """Abort if request status has already 
    been accepted: update not possible
    """
    req = get_ride_request(reqID)
    if req.status == "Accepted":
        msg="Ride Request Cannot be changed: already accpeted"
        abort(HTTPStatus.FORBIDDEN, message=msg)


def abort_not_request_owner(reqID, user):
    """Abort if the user is not the 
    owner of the request
    """

    req = get_ride_request(reqID)
    if req.user_id != user:
        msg = "You are not authorized to view this requests"
        abort(HTTPStatus.UNAUTHORIZED, message=msg)