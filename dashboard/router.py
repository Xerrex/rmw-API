from typing import List
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from auth.deps_auth import get_current_user
from auth.schemas import UserSchema
from db.db_deps import get_db
from .crud_dashboard import (
    get_dashboard_metrics,
    get_upcoming_rides,
    get_dashboard_ride_requests,
    get_dashboard_activity,
)
from .schemas import (
    DashboardMetricSchema,
    UpcomingRideSchema,
    RideRequestDashboardSchema,
    ActivityItemSchema,
)

router = APIRouter()


@router.get("/metrics", response_model=List[DashboardMetricSchema])
def get_metrics(
    db: Session = Depends(get_db),
    current_user: UserSchema = Depends(get_current_user),
):
    """Get aggregate metrics for the dashboard."""
    return get_dashboard_metrics(db=db, user_id=current_user.id)


@router.get("/upcoming-rides", response_model=List[UpcomingRideSchema])
def get_upcoming(
    db: Session = Depends(get_db),
    current_user: UserSchema = Depends(get_current_user),
):
    """Get upcoming rides for the logged-in user."""
    return get_upcoming_rides(db=db, user_id=current_user.id)


@router.get("/ride-requests", response_model=List[RideRequestDashboardSchema])
def get_ride_requests(
    db: Session = Depends(get_db),
    current_user: UserSchema = Depends(get_current_user),
):
    """Get recent ride requests relevant to the logged-in user."""
    return get_dashboard_ride_requests(db=db, user_id=current_user.id)


@router.get("/activity", response_model=List[ActivityItemSchema])
def get_activity(
    db: Session = Depends(get_db),
    current_user: UserSchema = Depends(get_current_user),
):
    """Get recent activity events for the logged-in user."""
    return get_dashboard_activity(db=db, user_id=current_user.id)
