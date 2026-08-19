from datetime import datetime
from typing import List, Optional
from pydantic import BaseModel, ConfigDict, model_validator


class Ride_RequestCreateSchema(BaseModel):
    seats: int
    pickup: str
    stop: str
    # Names of the occupants of the extra seats (seats - 1), required when seats > 1
    passenger_names: Optional[List[str]] = None

    @model_validator(mode="after")
    def validate_passenger_names(self):
        required = max(self.seats - 1, 0)
        names = [n.strip() for n in (self.passenger_names or []) if n and n.strip()]
        if len(names) != required:
            raise ValueError(
                f"Provide exactly {required} passenger name(s) for the additional seat(s)."
            )
        self.passenger_names = names
        return self


class RideSummarySchema(BaseModel):
    uuid: str
    vehicle_plate: str
    vehicle_model: str
    town_starting: str
    town_ending: str
    depart_time: datetime
    end_time: datetime
    status: str

    model_config = ConfigDict(from_attributes=True)


class Ride_RequestSchema(BaseModel):
    id: int
    uuid: str
    seats: int
    pickup: str
    stop: str
    status: str
    created_at: datetime
    updated_at: datetime
    ride_id: int
    ride: Optional[RideSummarySchema] = None
    ride_requester_id: int
    requester_name: Optional[str] = None
    # "requester" if the viewer made the request, "owner" if it was made on the viewer's ride
    viewer_role: Optional[str] = None
    can_edit: bool = False
    # Only populated for the ride owner
    passenger_names: Optional[List[str]] = None

    model_config = ConfigDict(
        from_attributes=True,
        json_encoders={
            datetime: lambda v: v.strftime("%d-%m-%Y %H:%M")  # Custom datetime serialization
        }
    )


class Ride_RequestUpdateSchema(BaseModel):
    seats: int
    pickup: str
    stop: str
    passenger_names: Optional[List[str]] = None

    @model_validator(mode="after")
    def validate_passenger_names(self):
        required = max(self.seats - 1, 0)
        names = [n.strip() for n in (self.passenger_names or []) if n and n.strip()]
        if len(names) != required:
            raise ValueError(
                f"Provide exactly {required} passenger name(s) for the additional seat(s)."
            )
        self.passenger_names = names
        return self

