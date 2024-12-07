from sqlalchemy.orm import Session
from db.models import Ride
from .schemas_rides import RideCreateSchema, RideUpdateSchema


def get_rides(db: Session, skip: int=0, limit: int=5000):
    """Get all rides

    Args:
        db (Session): Database session.
        skip (int, optional): The number of records to skip. Defaults to 0.
        limit (int, optional): The maximum number of records to retrieve. Defaults to 5000.
    
    Returns:
        List[Ride]: A list of all rides objects in the database.
    """
    rides = db.query(Ride).order_by(Ride.id).offset(skip).limit(limit).all()
    return(rides)


def get_ride_by_uuid(uuid: str, db:Session):
    """Get ride by uuid

    Args:
        uuid (str): A string representing a uuid.
        db (Session): Database session.
    
    Returns:
        Ride: A database object representing a ride.
    """

    ride = db.query(Ride).filter(Ride.uuid == uuid).first()
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

    new_ride = Ride()
    new_ride.vehicle_plate = rideData.vehicle_plate
    new_ride.seats = rideData.seats
    new_ride.town_starting =  rideData.town_starting
    new_ride.town_ending = rideData.town_ending
    new_ride.depart_time = rideData.depart_time
    new_ride.end_time = rideData.end_time
    new_ride.owner_id = owner_id

    db.add(new_ride)
    db.commit()
    db.refresh(new_ride)
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

    ride.seats = rideData.seats
    ride.town_starting = rideData.town_starting
    ride.town_ending = rideData.town_ending
    ride.depart_time = rideData.depart_time
    ride.end_time = rideData.end_time

    db.add(ride)
    db.commit()
    db.refresh(ride)
    return ride
   