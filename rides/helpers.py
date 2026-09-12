"""Viewer-specific ride computations shared by the rides router.

Keeps seat availability, ownership, and request-visibility rules in one place
so both the rides list and ride-detail endpoints stay consistent.
"""
import json
from datetime import datetime, timezone, timedelta
from typing import Optional
from db.models import Ride, RideRequest, AuditLog

ACCEPTED_STATUS = "Accepted"
PENDING_STATUS = "Pending"
REJECTED_STATUS = "Rejected"

# Requests can no longer be edited once the ride is within this window of departing
EDIT_CUTOFF = timedelta(hours=6)


def get_accepted_seats(ride: Ride) -> int:
    """Total seats already confirmed (accepted) on a ride."""
    return sum(req.seats for req in ride.ride_requests if req.status == ACCEPTED_STATUS)


def get_available_seats(ride: Ride) -> int:
    """Seats still open for booking once accepted requests are subtracted."""
    return max(ride.seats - get_accepted_seats(ride), 0)


def get_pending_requests_count(ride: Ride) -> int:
    """Number of requests still awaiting the owner's decision."""
    return sum(1 for req in ride.ride_requests if req.status == PENDING_STATUS)


def user_has_requested(ride: Ride, user_id: int) -> bool:
    """Whether the given user has an active (non-rejected) request on the ride."""
    return any(
        req.ride_requester_id == user_id and req.status != REJECTED_STATUS
        for req in ride.ride_requests
    )


def can_edit_ride_request(ride_request: RideRequest) -> bool:
    """Whether a ride request's details (seats/pickup/stop) can still be changed.

    Allowed only while the request is not yet accepted and the ride is still
    upcoming and more than EDIT_CUTOFF away from departing.
    """
    ride = ride_request.ride
    if ride_request.status == ACCEPTED_STATUS:
        return False
    if not ride or ride.status != "upcoming":
        return False

    depart_time = ride.depart_time
    if depart_time.tzinfo is None:
        depart_time = depart_time.replace(tzinfo=timezone.utc)
    return depart_time - datetime.now(timezone.utc) >= EDIT_CUTOFF


def serialize_ride(ride: Ride, current_user_id: int) -> dict:
    """Combine ORM ride fields with viewer-specific context for API responses."""
    is_owner = ride.owner_id == current_user_id
    owner = ride.owner
    vehicle = ride.vehicle

    vehicle_plate = vehicle.vehicle_plate if vehicle else "N/A"
    vehicle_model = vehicle.vehicle_model if vehicle else "N/A"

    return {
        "id": ride.id,
        "uuid": ride.uuid,
        "vehicle_uuid": ride.vehicle_uuid,
        "vehicle_plate": vehicle_plate,
        "vehicle_model": vehicle_model,
        "seats": ride.seats,
        "town_starting": ride.town_starting,
        "town_ending": ride.town_ending,
        "depart_time": ride.depart_time,
        "end_time": ride.end_time,
        "status": ride.status,
        "created_at": ride.created_at,
        "updated_at": ride.updated_at,
        "owner_name": f"{owner.first_name} {owner.last_name}" if owner else None,
        "available_seats": get_available_seats(ride),
        "is_owner": is_owner,
        "pending_requests_count": get_pending_requests_count(ride) if is_owner else None,
        "has_requested": None if is_owner else user_has_requested(ride, current_user_id),
    }


def serialize_ride_request(ride_request: RideRequest, current_user_id: Optional[int] = None) -> dict:
    """Combine ORM ride-request fields with the requester's display name.

    When current_user_id is supplied, also annotate viewer-specific context:
    whether the viewer owns the ride ("owner") or made the request
    ("requester"), whether they can still edit the request, and the
    passenger names (visible to the requester always, and to the owner only
    once the request has been accepted).
    """
    requester = ride_request.ride_requester
    ride = ride_request.ride
    is_owner = bool(ride and current_user_id is not None and ride.owner_id == current_user_id)
    viewer_role = None
    if current_user_id is not None:
        viewer_role = "owner" if is_owner else "requester"

    passenger_names = json.loads(ride_request.passenger_names) if ride_request.passenger_names else []

    ride_vehicle = ride.vehicle if ride else None
    vehicle_plate = ride_vehicle.vehicle_plate if ride_vehicle else "N/A"
    vehicle_model = ride_vehicle.vehicle_model if ride_vehicle else "N/A"

    return {
        "id": ride_request.id,
        "uuid": ride_request.uuid,
        "seats": ride_request.seats,
        "pickup": ride_request.pickup,
        "stop": ride_request.stop,
        "status": ride_request.status,
        "created_at": ride_request.created_at,
        "updated_at": ride_request.updated_at,
        "ride": {
            "uuid": ride.uuid,
            "vehicle_uuid": ride.vehicle_uuid,
            "vehicle_plate": vehicle_plate,
            "vehicle_model": vehicle_model,
            "town_starting": ride.town_starting,
            "town_ending": ride.town_ending,
            "depart_time": ride.depart_time,
            "end_time": ride.end_time,
            "status": ride.status,
        } if ride else None,
        "ride_id": ride_request.ride_id,
        "ride_requester_id": ride_request.ride_requester_id,
        "requester_name": f"{requester.first_name} {requester.last_name}" if requester else None,
        "viewer_role": viewer_role,
        "can_edit": (not is_owner) and can_edit_ride_request(ride_request),
        "passenger_names": passenger_names if (not is_owner or ride_request.status == ACCEPTED_STATUS) else None,
    }


def serialize_audit_log(entry: AuditLog) -> dict:
    """Combine ORM audit log fields with the actor's display name."""
    actor = entry.actor
    return {
        "id": entry.id,
        "entity_type": entry.entity_type,
        "entity_uuid": entry.entity_uuid,
        "action": entry.action,
        "changes": json.loads(entry.changes) if entry.changes else None,
        "actor_name": f"{actor.first_name} {actor.last_name}" if actor else None,
        "created_at": entry.created_at,
    }


def make_aware(dt: Optional[datetime]) -> Optional[datetime]:
    if dt is None:
        return None
    if dt.tzinfo is None:
        return dt.replace(tzinfo=timezone.utc)
    return dt.astimezone(timezone.utc)


def auto_update_expired_rides_and_requests(db) -> None:
    """Automatically update ride requests and ride statuses based on current time.

    1. Pending requests on rides whose depart_time has passed are marked as Rejected
       and logged in audit logs.
    2. Rides whose end_time + 12 hours has passed (and status is still 'upcoming')
       are marked as 'completed' and logged in audit logs.
    """
    from .audit import log_action

    now = datetime.now(timezone.utc)

    # 1. Pending requests on rides whose depart_time has passed -> mark as Rejected
    pending_requests = (
        db.query(RideRequest)
        .join(RideRequest.ride)
        .filter(RideRequest.status == PENDING_STATUS)
        .all()
    )

    has_changes = False
    for req in pending_requests:
        if req.ride and req.ride.depart_time:
            depart_time_aware = make_aware(req.ride.depart_time)
            if depart_time_aware and depart_time_aware <= now:
                req.status = REJECTED_STATUS
                db.add(req)
                log_action(
                    db,
                    entity_type="ride_request",
                    entity_uuid=req.uuid,
                    action="status_changed",
                    actor_id=None,
                    changes={
                        "status": {"from": PENDING_STATUS, "to": REJECTED_STATUS},
                        "reason": "auto_rejected_depart_time_passed",
                    },
                )
                has_changes = True

    # 2 & 3. Upcoming rides whose end_time + 12 hours has passed -> mark as completed
    cutoff_time = now - timedelta(hours=12)
    upcoming_rides = (
        db.query(Ride)
        .filter(Ride.status == "upcoming")
        .all()
    )

    for ride in upcoming_rides:
        if ride.end_time:
            end_time_aware = make_aware(ride.end_time)
            if end_time_aware and end_time_aware <= cutoff_time:
                ride.status = "completed"
                db.add(ride)
                log_action(
                    db,
                    entity_type="ride",
                    entity_uuid=ride.uuid,
                    action="status_changed",
                    actor_id=None,
                    changes={
                        "status": {"from": "upcoming", "to": "completed"},
                        "reason": "auto_completed_end_time_passed_12h",
                    },
                )
                has_changes = True

    if has_changes:
        db.commit()

