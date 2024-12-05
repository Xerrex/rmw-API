from datetime import datetime
from typing import List
from pydantic import BaseModel


class RideSchema(BaseModel):
    id: int
    uuid: str
    vehicle_plate: str
    seats: int
    town_starting: str
    town_ending: str
    depart_time: datetime
    end_time: datetime
    created_at: datetime
    updated_at: datetime
    owner_id: int

    class Config:
        from_attributes = True
        orm_mode = True


class RidesSchema(BaseModel):
    rides: List[RideSchema]


class RideCreateSchema(BaseModel):
    vehicle_plate: str
    seats: int
    town_starting: str
    town_ending: str
    depart_time: datetime
    end_time: datetime
    # owner_id


class RideUpdateSchema(BaseModel):
    seats: int
    town_starting: str
    town_ending: str
    depart_time: datetime
    end_time: datetime