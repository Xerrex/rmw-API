from datetime import datetime
from typing import Optional
from fastapi import HTTPException
from sqlalchemy import or_
from sqlalchemy.orm import Session, joinedload, selectinload
from db.models import Ride, Vehicle
from .schemas_rides import RideCreateSchema, RideUpdateSchema
from .audit import log_action, diff_fields


def get_rides(db: Session, skip: int = 0, limit: int = 5000, search: Optional[str] = None,
              min_seats: Optional[int] = None, date_from: Optional[datetime] = None,
              date_to: Optional[datetime] = None):
    """Get all rides

    Args:
        db (Session): Database session.
        skip (int, optional): The number of records to skip. Defaults to 0.
        limit (int, optional): The maximum number of records to retrieve. Defaults to 5000.
        search (str, optional): Matches against vehicle plate/model or town starting/ending.
        min_seats (int, optional): Minimum number of available seats.
        date_from (datetime, optional): Only rides departing on/after this datetime.
        date_to (datetime, optional): Only rides departing on/before this datetime.
    
    Returns:
        tuple[List[Ride], int]: A list of matching ride objects and the total match count.
    """
    query = db.query(Ride).options(
        selectinload(Ride.ride_requests),
        joinedload(Ride.owner),
        joinedload(Ride.vehicle),
    )

    if search:
        like = f"%{search}%"
        query = query.outerjoin(Ride.vehicle).filter(or_(
            Vehicle.vehicle_plate.ilike(like),
            Vehicle.vehicle_model.ilike(like),
            Ride.town_starting.ilike(like),
            Ride.town_ending.ilike(like),
        ))

    if min_seats is not None:
        query = query.filter(Ride.seats >= min_seats)

    if date_from is not None:
        query = query.filter(Ride.depart_time >= date_from)

    if date_to is not None:
        query = query.filter(Ride.depart_time <= date_to)

    total = query.count()
    rides = query.order_by(Ride.id).offset(skip).limit(limit).all()
    return rides, total



def get_ride_by_uuid(uuid: str, db:Session):
    """Get ride by uuid

    Args:
        uuid (str): A string representing a uuid.
        db (Session): Database session.
    
    Returns:
        Ride: A database object representing a ride.
    """
    ride = db.query(Ride).options(
        selectinload(Ride.ride_requests),
        joinedload(Ride.owner),
        joinedload(Ride.vehicle),
    ).filter(Ride.uuid == uuid).first()
    return ride


def create_ride(owner_id: int, rideData: RideCreateSchema, db:Session):
    """Creates a ride
    
    saves a new ride to the database.

    Args:
        owner_id (int): user id of the owner of the ride.
        rideData (RideCreateSchema): Data to create a ride.
        db (Session): Database session.

    Returns:
        Ride: A database object representing a ride.
    """
    vehicle = None
    if rideData.vehicle_uuid:
        vehicle = db.query(Vehicle).filter(Vehicle.uuid == rideData.vehicle_uuid, Vehicle.owner_id == owner_id).first()
        if not vehicle:
            raise HTTPException(status_code=400, detail="Vehicle not found or does not belong to user")

    new_ride = Ride()
    if vehicle:
        new_ride.vehicle_uuid = vehicle.uuid

    new_ride.seats = rideData.seats
    new_ride.town_starting =  rideData.town_starting
    new_ride.town_ending = rideData.town_ending
    new_ride.depart_time = rideData.depart_time
    new_ride.end_time = rideData.end_time
    new_ride.owner_id = owner_id

    db.add(new_ride)
    db.commit()
    db.refresh(new_ride)

    log_action(db, entity_type="ride", entity_uuid=new_ride.uuid, action="created", actor_id=owner_id)
    return new_ride


def update_ride(ride: Ride, rideData:RideUpdateSchema, db:Session):
    """Update a ride

    Args:
        ride (Ride): A database object representing a ride.
        rideData (RideUpdateSchema): Data to update a ride.
        db (Session): Database session.
    Returns:
        Ride: A database object representing a ride.
    """

    before = {
        "seats": ride.seats,
        "town_starting": ride.town_starting,
        "town_ending": ride.town_ending,
        "depart_time": ride.depart_time,
        "end_time": ride.end_time,
        "status": ride.status,
    }

    ride.seats = rideData.seats
    ride.town_starting = rideData.town_starting
    ride.town_ending = rideData.town_ending
    ride.depart_time = rideData.depart_time
    ride.end_time = rideData.end_time
    if rideData.status is not None:
        ride.status = rideData.status.value

    db.add(ride)
    db.commit()
    db.refresh(ride)

    after = {
        "seats": ride.seats,
        "town_starting": ride.town_starting,
        "town_ending": ride.town_ending,
        "depart_time": ride.depart_time,
        "end_time": ride.end_time,
        "status": ride.status,
    }
    log_action(db, entity_type="ride", entity_uuid=ride.uuid, action="updated",
               actor_id=ride.owner_id, changes=diff_fields(before, after))
    return ride
   