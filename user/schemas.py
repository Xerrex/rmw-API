from datetime import datetime
from typing import Optional
from pydantic import BaseModel, ConfigDict, Field


class VehicleSchema(BaseModel):
    id: int
    uuid: str
    vehicle_plate: str
    vehicle_model: str
    seats: int
    owner_id: int
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(
        from_attributes=True,
        json_encoders={
            datetime: lambda v: v.strftime("%d-%m-%Y %H:%M")
        }
    )


class VehicleCreateSchema(BaseModel):
    vehicle_plate: str = Field(..., min_length=1)
    vehicle_model: str = Field(..., min_length=1)
    seats: int = Field(4, ge=1)


class ChangePasswordSchema(BaseModel):
    current_password: str = Field(..., min_length=1)
    new_password: str = Field(..., min_length=6)
