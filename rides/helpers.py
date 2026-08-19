"""Viewer-specific ride computations shared by the rides router.

Keeps seat availability, ownership, and request-visibility rules in one place
so both the rides list and ride-detail endpoints stay consistent.
"""
from typing import Optional
from db.models import Ride, RideRequest

ACCEPTED_STATUS = "Accepted"
PENDING_STATUS = "Pending"
REJECTED_STATUS = "Rejected"


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


def serialize_ride(ride: Ride, current_user_id: int) -> dict:
    """Combine ORM ride fields with viewer-specific context for API responses."""
    is_owner = ride.owner_id == current_user_id
    owner = ride.owner

    return {
        "id": ride.id,
        "uuid": ride.uuid,
        "vehicle_plate": ride.vehicle_plate,
        "vehicle_model": ride.vehicle_model,
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


def serialize_ride_request(ride_request: RideRequest) -> dict:
    """Combine ORM ride-request fields with the requester's display name."""
    requester = ride_request.ride_requester
    ride = ride_request.ride
    return {
        # "id": ride_request.id,
        "uuid": ride_request.uuid,
        "seats": ride_request.seats,
        "pickup": ride_request.pickup,
        "stop": ride_request.stop,
        "status": ride_request.status,
        "created_at": ride_request.created_at,
        "updated_at": ride_request.updated_at,
        "ride": {
            "uuid": ride.uuid,
            "vehicle_plate": ride.vehicle_plate,
            "vehicle_model": ride.vehicle_model,
            "town_starting": ride.town_starting,
            "town_ending": ride.town_ending,
            "depart_time": ride.depart_time,
            "end_time": ride.end_time,
            "status": ride.status,
        } if ride else None,
        # "ride_id": ride_request.ride_id,
        # "ride_requester_id": ride_request.ride_requester_id,
        "requester_name": f"{requester.first_name} {requester.last_name}" if requester else None,
    }
