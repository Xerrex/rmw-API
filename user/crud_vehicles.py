from typing import List, Optional
from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from db.models import Vehicle, Ride
from .schemas import VehicleCreateSchema


def get_user_vehicles(db: Session, user_id: int) -> List[Vehicle]:
    return db.query(Vehicle).filter(Vehicle.owner_id == user_id).order_by(Vehicle.id.desc()).all()


def get_vehicle_by_id(db: Session, vehicle_id: int) -> Optional[Vehicle]:
    return db.query(Vehicle).filter(Vehicle.id == vehicle_id).first()


def create_user_vehicle(db: Session, user_id: int, data: VehicleCreateSchema) -> Vehicle:
    vehicle = Vehicle(
        vehicle_plate=data.vehicle_plate.strip(),
        vehicle_model=data.vehicle_model.strip(),
        seats=data.seats,
        owner_id=user_id,
    )
    db.add(vehicle)
    db.commit()
    db.refresh(vehicle)
    return vehicle


def delete_user_vehicle(db: Session, user_id: int, vehicle_id: int) -> None:
    vehicle = db.query(Vehicle).filter(Vehicle.id == vehicle_id).first()
    if not vehicle:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Vehicle not found")

    if vehicle.owner_id != user_id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="You are not authorized to delete this vehicle")

    # Deleting a vehicle should be possible if there is no ride created using the vehicle details, otherwise it should not be possible.
    ride_count = db.query(Ride).filter(Ride.vehicle_uuid == vehicle.uuid).count()
    if ride_count > 0:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Cannot delete this vehicle because it has been used to create one or more rides."
        )

    db.delete(vehicle)
    db.commit()
