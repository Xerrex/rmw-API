from datetime import datetime
from typing import Optional
from pydantic import BaseModel, ConfigDict


class Ride_RequestCreateSchema(BaseModel):
    seats: int
    stop: str
    # status: str = "Pending"
    # ride_id: int
    # ride_requester_id: int


class Ride_RequestSchema(BaseModel):
    id: int
    uuid: str
    seats: int
    stop: str
    status: str
    created_at: datetime
    updated_at: datetime
    ride_id: int
    # ride
    ride_requester_id: int
    requester_name: Optional[str] = None

    model_config = ConfigDict(
        from_attributes=True,
        json_encoders={
            datetime: lambda v: v.strftime("%d-%m-%Y %H:%M")  # Custom datetime serialization
        }
    )


class Ride_RequestUpdateSchema(BaseModel):
    seats: int
    stop: str
