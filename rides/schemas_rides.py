from datetime import datetime
from enum import Enum
from typing import List, Optional
from pydantic import BaseModel, field_validator, model_validator, ConfigDict


class RideStatus(str, Enum):
    upcoming = "upcoming"
    completed = "completed"
    rescheduled = "rescheduled"
    canceled = "canceled"


class RideSchema(BaseModel):
    id: int
    uuid: str
    vehicle_plate: str
    vehicle_model: str
    seats: int
    town_starting: str
    town_ending: str
    depart_time: datetime
    end_time: datetime
    status: RideStatus
    created_at: datetime
    updated_at: datetime
    # owner_id: int
    
    model_config = ConfigDict(
        from_attributes=True,
        json_encoders={
            datetime: lambda v: v.strftime("%d-%m-%Y %H:%M")  # Custom datetime serialization
        },
        json_schema_extra={
            "example": {
                "id": 0,
                "uuid": "string",
                "vehicle_plate": "KXX 123X",
                "vehicle_model": "Nissan Note",
                "seats": 4,
                "town_starting": "Nairobi",
                "town_ending": "Mombasa",
                "depart_time": "01-12-2024 08:00",
                "end_time": "01-12-2024 12:00",
                "status": "upcoming",
                "created_at": "06-12-2024 07:45",
                "updated_at": "06-12-2024 07:45",
                "owner_id": 0
            }
        },
    )


class RidesSchema(BaseModel):
    rides: List[RideSchema]
    total: int
    page: int
    limit: int


class RideDetailsSchema(BaseModel):
    depart_time: datetime
    end_time: datetime

    @field_validator("depart_time", "end_time", mode="before")
    def validate_datetime_format(cls, value):
        """
        Validates and parses datetime in the format 'dd-mm-yyyy hh:mm' or ISO 8601.
        ie. 20-12-2024 08:00 or 2024-12-20T08:00
        """
        if isinstance(value, str):
            try:
                return datetime.strptime(value, "%d-%m-%Y %H:%M")
            except ValueError:
                try:
                    return datetime.fromisoformat(value)
                except ValueError:
                    raise ValueError(
                        "Invalid datetime format. Use 'dd-mm-yyyy hh:mm' or ISO 8601."
                    )
        return value

    @model_validator(mode="after")
    def validate_end_after_depart(self):
        if self.end_time <= self.depart_time:
            raise ValueError("end_time must be later than depart_time.")
        return self
    


class RideCreateSchema(RideDetailsSchema):
    vehicle_plate: str
    vehicle_model: str
    seats: int
    town_starting: str
    town_ending: str
    

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "vehicle_plate": "KXX 123X",
                "vehicle_model": "Nissan Note",
                "seats": 4,
                "town_starting": "Nairobi",
                "town_ending": "Mombasa",
                "depart_time": "01-12-2024 08:00",
                "end_time": "01-12-2024 12:00"
            }
        },
        json_encoders={
            datetime: lambda v: v.strftime("%d-%m-%Y %H:%M")
        }
    )


class RideUpdateSchema(RideDetailsSchema):
    vehicle_model: str
    seats: int
    town_starting: str
    town_ending: str
    status: Optional[RideStatus] = None

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "town_starting": "Nairobi",
                "town_ending": "Mombasa",
                "depart_time": "01-12-2024 08:00",
                "end_time": "01-12-2024 12:00",
                "seats": 4,
                "vehicle_model": "Nissan Note",
                "status": "upcoming",
            }
        },
    )
