from datetime import datetime
from typing import Optional
import json
from sqlalchemy.orm import Session, joinedload, selectinload
from sqlalchemy import or_
from db.models import RideRequest, Ride
from .schemas_rides_requests import Ride_RequestCreateSchema, Ride_RequestUpdateSchema
from .audit import log_action, diff_fields
from .helpers import PENDING_STATUS


def get_all_user_requests(user_id: int, db: Session, skip: int=0, limit: int=5000,
                          search: Optional[str] = None,  min_seats: Optional[int] = None, date_from: Optional[datetime] = None, date_to: Optional[datetime] = None):
    """Get requests relevant to a user: requests they made, and requests made on rides they own.

    Args:
        user_id (int): The id of the viewer.
        db (Session): Database session.
        skip (int, optional): The number of records to skip. Defaults to 0.
        limit (int, optional): The maximum number of records to retrieve. Defaults to 5000.
        search (str, optional): Matches against vehicle plate/model or town starting/ending.
        min_seats (int, optional): Minimum number of available seats.
        date_from (datetime, optional): Only rides departing on/after this datetime.
        date_to (datetime, optional): Only rides departing on/before this datetime.

    Returns:
        List[RideRequest]: A list of all ride requests objects in the database.
    """
    query = db.query(RideRequest).join(RideRequest.ride).options(
        selectinload(RideRequest.ride),
        joinedload(RideRequest.ride_requester),
    ).filter(or_(
        RideRequest.ride_requester_id == user_id,
        Ride.owner_id == user_id,
    ))

    if search:
        like = f"%{search}%"
        query = query.filter(or_(
                Ride.vehicle_plate.ilike(like),
                Ride.vehicle_model.ilike(like),
                Ride.town_starting.ilike(like),
                Ride.town_ending.ilike(like),
            ))

    if min_seats is not None:
        query = query.filter(RideRequest.seats >= min_seats)

    if date_from is not None:
        query = query.filter(Ride.depart_time >= date_from)

    if date_to is not None:
        query = query.filter(Ride.depart_time <= date_to)

    total = query.count()
    r_requests = query.order_by(RideRequest.id).offset(skip).limit(limit).all()
    return r_requests, total


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
    new_ride_request.passenger_names = json.dumps(rideRequestData.passenger_names or [])
    new_ride_request.ride_id = ride_id
    new_ride_request.ride_requester_id = ride_requester_id

    db.add(new_ride_request)
    db.commit()
    db.refresh(new_ride_request)

    log_action(db, entity_type="ride_request", entity_uuid=new_ride_request.uuid,
               action="created", actor_id=ride_requester_id,
               changes={"seats": {"from": None, "to": new_ride_request.seats},
                        "pickup": {"from": None, "to": new_ride_request.pickup},
                        "stop": {"from": None, "to": new_ride_request.stop}})
    return new_ride_request


def update_ride_request(db: Session, ride_request: RideRequest, rideRequestData: Ride_RequestUpdateSchema,
                         actor_id: Optional[int] = None):
    """Update ride request

    Updating the details of a request resets it to Pending, since the owner
    needs to re-evaluate the new details.

    Args:
        db (Session): Database session.
        ride_request (RideRequest): A database object representing a ride-request.
        rideRequestData (Ride_RequestUpdateSchema): Data to update a ride request.
        actor_id (int, optional): id of the user performing the update, for audit purposes.
    
    Returns:
        RideRequest: A database object representing a ride-request.
    """
    before = {
        "seats": ride_request.seats,
        "pickup": ride_request.pickup,
        "stop": ride_request.stop,
        "status": ride_request.status,
    }

    ride_request.seats = rideRequestData.seats
    ride_request.pickup = rideRequestData.pickup
    ride_request.stop = rideRequestData.stop
    ride_request.passenger_names = json.dumps(rideRequestData.passenger_names or [])
    ride_request.status = PENDING_STATUS

    db.add(ride_request)
    db.commit()
    db.refresh(ride_request)

    after = {
        "seats": ride_request.seats,
        "pickup": ride_request.pickup,
        "stop": ride_request.stop,
        "status": ride_request.status,
    }
    log_action(db, entity_type="ride_request", entity_uuid=ride_request.uuid,
               action="updated", actor_id=actor_id, changes=diff_fields(before, after))
    return ride_request


def  update_request_status(db: Session, ride_request: RideRequest, rideRequestStatus: str,
                            actor_id: Optional[int] = None):
    """Update request status

    Args:
        db (Session): Database session.
        ride_request (RideRequest): A database object representing a ride-request.
        rideRequestStatus (str): New status ("Accepted"/"Rejected").
        actor_id (int, optional): id of the user performing the update, for audit purposes.
    """
    before_status = ride_request.status
    ride_request.status = rideRequestStatus
    db.add(ride_request)
    db.commit()
    db.refresh(ride_request)

    log_action(db, entity_type="ride_request", entity_uuid=ride_request.uuid,
               action="status_changed", actor_id=actor_id,
               changes={"status": {"from": before_status, "to": ride_request.status}})
    return ride_request


