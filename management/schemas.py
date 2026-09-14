from typing import List, Optional
from datetime import datetime
from pydantic import BaseModel, EmailStr


class RideStatSchema(BaseModel):
    date: str
    completed: int
    cancelled: int


class StatusDistributionSchema(BaseModel):
    status: str
    count: int


class AnalyticsSchema(BaseModel):
    total_rides: int
    total_requests: int
    total_passengers: int
    active_drivers: int
    rides_over_time: List[RideStatSchema]
    status_distribution: List[StatusDistributionSchema]


class ManagedUserSchema(BaseModel):
    id: int
    uuid: str
    first_name: str
    last_name: str
    email: EmailStr
    role: str
    created_at: datetime

    class Config:
        from_attributes = True


class UpdateUserRoleSchema(BaseModel):
    role: str


VALID_ROLES = ("user", "staff", "admin")
