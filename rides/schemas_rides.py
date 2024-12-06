from datetime import datetime
from typing import List
from pydantic import BaseModel, field_validator, ConfigDict


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
    
    model_config = ConfigDict(
        from_attributes=True,  # Enable compatibility with ORM models
        json_encoders={
            datetime: lambda v: v.strftime("%d-%m-%Y %H:%M")  # Custom datetime serialization
        },
        json_schema_extra={
            "example": {
                "id": 0,
                "uuid": "string",
                "vehicle_plate": "KXX 123X",
                "seats": 4,
                "town_starting": "Nairobi",
                "town_ending": "Mombasa",
                "depart_time": "01-12-2024 08:00",
                "end_time": "01-12-2024 12:00",
                "created_at": "06-12-2024 07:45",
                "updated_at": "06-12-2024 07:45",
                "owner_id": 0
            }
        },
    )


class RidesSchema(BaseModel):
    rides: List[RideSchema]


class RideDetailsSchema(BaseModel):
    depart_time: datetime
    end_time: datetime

    @field_validator("depart_time", "end_time", mode="before")
    def validate_datetime_format(cls, value):
        """
        Validates and parses datetime in the format 'dd-mm-yyyy hh:mm'.
        ie. 20-12-2024 08:00
        """
        if isinstance(value, str):
            try:
                return datetime.strptime(value, "%d-%m-%Y %H:%M")
            except ValueError:
                raise ValueError("Invalid datetime format. Use 'dd-mm-yyyy hh:mm'.")
        return value
    


class RideCreateSchema(RideDetailsSchema):
    vehicle_plate: str
    seats: int
    town_starting: str
    town_ending: str
    

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "vehicle_plate": "KXX 123X",
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
    seats: int
    town_starting: str
    town_ending: str

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "town_starting": "Nairobi",
                "town_ending": "Mombasa",
                "depart_time": "01-12-2024 08:00",
                "end_time": "01-12-2024 12:00",
                "seats": 4,
            }
        },
    )
