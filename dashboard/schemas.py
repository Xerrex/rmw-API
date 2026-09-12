from typing import List, Optional
from pydantic import BaseModel


class DashboardMetricSchema(BaseModel):
    id: str
    label: str
    value: str
    trendText: str
    trendUp: bool


class UpcomingRideSchema(BaseModel):
    id: str
    route: str
    startTown: str
    endTown: str
    startTime: str
    etaTime: str
    seatsAvailable: int
    vehicleNumber: str


class RideRequestDashboardSchema(BaseModel):
    id: str
    passengerName: str
    seatsRequested: int
    pickup: str
    dropOff: str
    route: str
    status: str


class ActivityItemSchema(BaseModel):
    id: str
    summary: str
    detail: str
    timestamp: str
