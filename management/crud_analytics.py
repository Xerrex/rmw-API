"""Aggregate queries powering the management analytics page."""
from datetime import datetime, timedelta, timezone
from typing import List
from sqlalchemy.orm import Session
from db.models import Ride, RideRequest, User


def get_analytics(db: Session) -> dict:
    total_rides = db.query(Ride).count()
    total_requests = db.query(RideRequest).count()
    total_passengers = (
        db.query(RideRequest.ride_requester_id).distinct().count()
    )
    active_drivers = (
        db.query(Ride.owner_id)
        .filter(Ride.status == "upcoming")
        .distinct()
        .count()
    )

    return {
        "total_rides": total_rides,
        "total_requests": total_requests,
        "total_passengers": total_passengers,
        "active_drivers": active_drivers,
        "rides_over_time": _get_rides_over_time(db),
        "status_distribution": _get_status_distribution(db),
    }


def _get_rides_over_time(db: Session, days: int = 7) -> List[dict]:
    """Rides completed vs ride requests rejected, per day, for the last `days` days."""
    now = datetime.now(timezone.utc)
    start = (now - timedelta(days=days - 1)).replace(hour=0, minute=0, second=0, microsecond=0)

    rides = db.query(Ride).filter(Ride.status == "completed", Ride.updated_at >= start).all()
    rejected_requests = db.query(RideRequest).filter(
        RideRequest.status == "Rejected", RideRequest.updated_at >= start
    ).all()

    buckets = {}
    for i in range(days):
        day = (start + timedelta(days=i)).date()
        buckets[day] = {"date": (start + timedelta(days=i)).strftime("%a"), "completed": 0, "cancelled": 0}

    for ride in rides:
        updated = ride.updated_at
        day = updated.date() if updated else None
        if day in buckets:
            buckets[day]["completed"] += 1

    for req in rejected_requests:
        updated = req.updated_at
        day = updated.date() if updated else None
        if day in buckets:
            buckets[day]["cancelled"] += 1

    return list(buckets.values())


def _get_status_distribution(db: Session) -> List[dict]:
    statuses = ["Pending", "Accepted", "Rejected"]
    return [
        {"status": status.lower(), "count": db.query(RideRequest).filter(RideRequest.status == status).count()}
        for status in statuses
    ]
