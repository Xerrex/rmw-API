from sqlalchemy.orm import Session
from db.models import RideRequest
from .schemas_rides_requests import Ride_RequestCreateSchema, Ride_RequestUpdateSchema


def get_requests_on_ride(db: Session, ride_id: int, skip: int=0, limit: int=5000):
    """Get ride requests

    Args:
        db (Session): Database session.
        skip (int, optional): The number of records to skip. Defaults to 0.
        limit (int, optional): The maximum number of records to retrieve. Defaults to 5000.
    
    Returns:
        List[RideRequest]: A list of all ride requests objects in the database.
    """
    ride_requests = db.query(RideRequest).filter(RideRequest.ride_id == ride_id).offset(skip).limit(limit).all()
    return ride_requests


def get_ride_request_by_uuid(db: Session, ride_request_uuid: str):
    """Get a ride-request by uuid
    
    Args:
        uuid (str): A string representing a uuid.
        db (Session): Database session.
    
    Returns:
        RideRequest: A database object representing a ride-request.
    """

    ride_request = db.query(RideRequest).filter(RideRequest.uuid == ride_request_uuid).first()
    return ride_request


def create_ride_request(db: Session, ride_id: int, ride_requester_id: int, 
                            rideRequestData: Ride_RequestCreateSchema):
    """Creates a ride-request

    saves a new ride request to the database.

    Args:
        db (Session): Database session.
        ride_id (int): id of ride on which to create a request on.
        ride_requester_id (int): user id of the person making a request.
        rideRequestData (Ride_RequestCreateSchema): Data to create a ride request.
    
    Returns:
        RideRequest: A database object representing a ride-request.
    """

    new_ride_request = RideRequest()
    new_ride_request.seats = rideRequestData.seats
    new_ride_request.pickup = rideRequestData.pickup
    new_ride_request.stop = rideRequestData.stop
    new_ride_request.ride_id = ride_id
    new_ride_request.ride_requester_id = ride_requester_id

    db.add(new_ride_request)
    db.commit()
    db.refresh(new_ride_request)
    return new_ride_request


def update_ride_request(db: Session, ride_request: RideRequest, rideRequestData: Ride_RequestUpdateSchema):
    """_Update ride request

    Args:
        db (Session): Database session.
        ride_request (RideRequest): A database object representing a ride-request.
        rideRequestData (Ride_RequestUpdateSchema): Data to update a ride request.
    
    Returns:
        RideRequest: A database object representing a ride-request.
    """
    
    ride_request.seats = rideRequestData.seats
    ride_request.stop = rideRequestData.stop

    db.add(ride_request)
    db.commit()
    db.refresh(ride_request)
    return ride_request


def  update_request_status(db: Session, ride_request: RideRequest, rideRequestStatus: str):
    """Update request status

    Args:
        db (Session): Database session.
        ride_request (RideRequest): A database object representing a ride-request.
        rideRequestData (Ride_RequestUpdateStatusSchema): Data to update a ride request status.
    """
    ride_request.status = rideRequestStatus
    db.add(ride_request)
    db.commit()
    db.refresh(ride_request)
    return ride_request

