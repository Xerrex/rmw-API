from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from auth.deps_auth import get_current_user
from auth.schemas import UserSchema
from db.db_deps import get_db
from .crud_rides import get_rides, create_ride, get_ride_by_uuid
from .schemas_rides import RidesSchema, RideCreateSchema, RideSchema


router = APIRouter()


@router.get("/", response_model=RidesSchema)
def get_all_rides(db:Session = Depends(get_db), _: any = Depends(get_current_user)):
    """Gets all rides
    """
    rides = get_rides(db=db)
    return {"rides": rides}


@router.post("/", response_model=RideSchema)
def create_new_ride(rideData: RideCreateSchema, db:Session = Depends(get_db), current_user: UserSchema = Depends(get_current_user)):
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


@router.put("/{ride_uuid}")
def update_ride_details(ride_uuid: str, db:Session = Depends(get_db), 
                        current_user: UserSchema = Depends(get_current_user)):
    """Update the details of a ride
    """
    pass


@router.get("/{ride_uuid}/requests")
def get_ride_requests(ride_uuid: str, db:Session = Depends(get_db), 
                      current_user: UserSchema = Depends(get_current_user)):
    """Get requests on a ride
    """
    pass


@router.post("/{ride_uuid}/requests")
def make_ride_requests(ride_uuid: str, db:Session = Depends(get_db), 
                       current_user: UserSchema = Depends(get_current_user)):
    """Make a request to join a ride.
    """
    pass


@router.get("/{ride_uuid}/requests/{request_uuid}")
def get_ride_request(ride_uuid: str, request_uuid: str, db:Session = Depends(get_db), 
                     current_user: UserSchema = Depends(get_current_user)):
    """get request on a ride..
    """
    pass


@router.put("/{ride_uuid}/requests/{request_uuid}")
def update_ride_request(ride_uuid: str, request_uuid: str, db:Session = Depends(get_db),
                        current_user: UserSchema = Depends(get_current_user)):
    """Update the details of a ride.
    """
    pass


@router.put("/{ride_uuid}/requests/{request_uuid}/status")
def update_ride_request_status(ride_uuid: str, request_uuid: str, db:Session = Depends(get_db), 
                               current_user: UserSchema = Depends(get_current_user)):
    """Update the status of a ride.
    status can be `Accepted/Rejected`
    """
    pass
