from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from auth.deps_auth import get_current_user
from auth.schemas import UserSchema
from db.db_deps import get_db
from .crud_rides import get_rides, create_ride, get_ride_by_uuid, \
    update_ride
from .crud_ride_requests import get_requests_on_ride, create_ride_request, \
                get_ride_request_by_uuid, update_ride_request, update_request_status

from .schemas_rides import RidesSchema, RideCreateSchema, RideSchema, \
    RideUpdateSchema
from .schemas_rides_requests import Ride_RequestSchema, Ride_RequestCreateSchema, \
    Ride_RequestUpdateSchema


router = APIRouter()


@router.get("/", response_model=RidesSchema)
def get_all_rides(db:Session = Depends(get_db), _: any = Depends(get_current_user)):
    """Gets all rides
    """
    rides = get_rides(db=db)
    return {"rides": rides}


@router.post("/", response_model=RideSchema)
def create_new_ride(rideData: RideCreateSchema, db:Session = Depends(get_db), 
                        current_user: UserSchema = Depends(get_current_user)):
    """Create a new ride
    """
    ride = create_ride(owner_id=current_user.id, rideData=rideData, db=db)
    return ride


@router.get("/{ride_uuid}", response_model=RideSchema)
def get_ride(ride_uuid: str, db:Session = Depends(get_db), _: any = Depends(get_current_user)):
    """Get ride
    """
    ride = get_ride_by_uuid(ride_uuid, db=db)
    return ride


@router.put("/{ride_uuid}", response_model=RideSchema)
def update_ride_details(ride_uuid: str, rideData: RideUpdateSchema, 
                        db:Session = Depends(get_db), current_user: UserSchema = Depends(get_current_user)):
    """Update the details of a ride
    """
    ride = get_ride_by_uuid(ride_uuid, db=db)

    if not ride:
        detail = f"Ride with uuid: '{ride_uuid}' does not exists."
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=detail)
    
    if ride.owner_id != current_user.id:
        detail = f"You are not authorized to update ride.: '{ride_uuid}'"
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=detail)
    
    updated_ride = update_ride(ride=ride, rideData=rideData, db=db)

    return updated_ride


@router.get("/{ride_uuid}/requests", response_model=List[Ride_RequestSchema])
def get_ride_requests(ride_uuid: str, db:Session = Depends(get_db), _: any = Depends(get_current_user)):
    """Get requests on a ride
    """
    ride = get_ride_by_uuid(ride_uuid, db=db)

    if not ride:
        detail = f"Ride with uuid: '{ride_uuid}' does not exists."
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=detail)
    
    ride_requests = get_requests_on_ride(db=db, ride_id=ride.id)
    return ride_requests



@router.post("/{ride_uuid}/requests", response_model=Ride_RequestSchema)
def make_ride_requests(ride_uuid: str, rideRequestData:Ride_RequestCreateSchema, 
                       db:Session = Depends(get_db), current_user: UserSchema = Depends(get_current_user)):
    """Make a request to join a ride.
    """
    ride = get_ride_by_uuid(ride_uuid, db=db)

    if not ride:
        detail = f"Ride with uuid: '{ride_uuid}' does not exists."
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=detail)
    
    if ride.owner_id == current_user.id:
        detail = f"You are not allowed to join this ride"
        raise HTTPException(status_code=status.HTTP_406_NOT_ACCEPTABLE, detail=detail)

    # TODo: Prevent requesting more than the available seats
    ride_request = create_ride_request(db=db, ride_id=ride.id, ride_requester_id=current_user.id, 
                                       rideRequestData=rideRequestData)
    
    return ride_request
    
    

@router.get("/{ride_uuid}/requests/{request_uuid}", response_model=Ride_RequestSchema)
def get_ride_request(ride_uuid: str, request_uuid: str, db:Session = Depends(get_db), 
                                                    _: any = Depends(get_current_user)):
    """get request on a ride..
    """
    ride = get_ride_by_uuid(ride_uuid, db=db)

    if not ride:
        detail = f"Ride with uuid: '{ride_uuid}' does not exists."
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=detail)
    

    ride_request = get_ride_request_by_uuid(db=db, ride_request_uuid=request_uuid)
    
    if not ride_request:
        detail = f"Ride request with uuid: '{request_uuid}' does not exists."
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=detail)
    
    return ride_request  


@router.put("/{ride_uuid}/requests/{request_uuid}", response_model=Ride_RequestSchema)
def update_ride_request_details(ride_uuid: str, request_uuid: str, rideRequestData:Ride_RequestUpdateSchema, 
                        db:Session = Depends(get_db), current_user: UserSchema = Depends(get_current_user)):
    """Update the details of a ride.
    """
    ride = get_ride_by_uuid(ride_uuid, db=db)

    if not ride:
        detail = f"Ride with uuid: '{ride_uuid}' does not exists."
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=detail)
    

    ride_request = get_ride_request_by_uuid(db=db, ride_request_uuid=request_uuid)
    
    if not ride_request:
        detail = f"Ride request with uuid: '{request_uuid}' does not exists."
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=detail)
    

    if ride_request.ride_requester_id != current_user.id:
        detail = f"You are not authorized to update ride request.: '{request_uuid}'"
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=detail)
    
    # TODO: Prevent Details update if ride request has been Accepted.

    updated_ride_request = update_ride_request(db=db, ride_request=ride_request, 
                                                    rideRequestData=rideRequestData)
    return updated_ride_request
    


@router.put("/{ride_uuid}/requests/{request_uuid}/status", response_model=Ride_RequestSchema)
def update_ride_request_status(ride_uuid: str, request_uuid: str, rideRequestStatus: str,
                               db:Session = Depends(get_db), current_user: UserSchema = Depends(get_current_user)):
    """Update the status of a ride.
    status can only be `Accepted/Rejected`
    """
    ride_requests_statuses = ["Accepted", "Rejected"]

    if rideRequestStatus not in ride_requests_statuses:
        detail = f'Ride request status is not among acceptable statues: {ride_requests_statuses}'
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=detail)

    ride = get_ride_by_uuid(ride_uuid, db=db)
    if not ride:
        detail = f"Ride with uuid: '{ride_uuid}' does not exists."
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=detail)
    
    ride_request = get_ride_request_by_uuid(db=db, ride_request_uuid=request_uuid)
    if not ride_request:
        detail = f"Ride request with uuid: '{request_uuid}' does not exists."
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=detail)
    

    if ride.owner_id != current_user.id:
        detail = f"You are not authorized to update ride request status: '{request_uuid}'"
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=detail)
    

    # TODO check if has reached maximum acceptance limit
    # TODO Reject all other ride requests with remarks that capacity has been reached.


    updated_ride_request = update_request_status(db=db, ride_request=ride_request, 
                                                rideRequestStatus=rideRequestStatus)
    
    return updated_ride_request
