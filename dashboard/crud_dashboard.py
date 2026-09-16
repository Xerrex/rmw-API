import json
from datetime import datetime, timezone
from typing import List
from sqlalchemy.orm import Session, joinedload
from sqlalchemy import or_
from db.models import Ride, RideRequest, AuditLog
from rides.crud_ride_requests import get_all_user_requests
from rides.helpers import get_available_seats, ACCEPTED_STATUS, PENDING_STATUS


def format_relative_time(dt: datetime) -> str:
    if dt is None:
        return ""
    if dt.tzinfo is None:
        dt = dt.replace(tzinfo=timezone.utc)
    now = datetime.now(timezone.utc)
    diff = now - dt
    seconds = int(diff.total_seconds())

    if seconds < 0 or seconds < 60:
        return "just now"
    minutes = seconds // 60
    if minutes < 60:
        return f"{minutes} minute{'s' if minutes != 1 else ''} ago"
    hours = minutes // 60
    if hours < 24:
        return f"{hours} hour{'s' if hours != 1 else ''} ago"
    days = hours // 24
    if days < 7:
        return f"{days} day{'s' if days != 1 else ''} ago"
    return dt.strftime("%b %d, %Y")


def get_dashboard_metrics(db: Session, user_id: int) -> List[dict]:
    # 1. Active rides (owned or joined)
    owned_active = db.query(Ride).filter(
        Ride.owner_id == user_id,
        Ride.status == "upcoming"
    ).count()

    joined_active = db.query(RideRequest).join(RideRequest.ride).filter(
        RideRequest.ride_requester_id == user_id,
        RideRequest.status == ACCEPTED_STATUS,
        Ride.status == "upcoming"
    ).count()

    active_rides_count = owned_active + joined_active

    # 2. Pending requests needing decision or response
    pending_requests_count = db.query(RideRequest).join(RideRequest.ride).filter(
        RideRequest.status == PENDING_STATUS,
        or_(
            RideRequest.ride_requester_id == user_id,
            Ride.owner_id == user_id
        )
    ).count()

    # 3. Completed trips
    owned_completed = db.query(Ride).filter(
        Ride.owner_id == user_id,
        or_(Ride.status == "completed", Ride.end_time < datetime.now(timezone.utc))
    ).count()

    joined_completed = db.query(RideRequest).join(RideRequest.ride).filter(
        RideRequest.ride_requester_id == user_id,
        RideRequest.status == ACCEPTED_STATUS,
        or_(Ride.status == "completed", Ride.end_time < datetime.now(timezone.utc))
    ).count()

    completed_trips_count = owned_completed + joined_completed

    # 4. Estimated community savings ($25 per completed or active shared trip)
    total_trips = completed_trips_count + active_rides_count
    savings_value = total_trips * 25

    return [
        {
            "id": "active-rides",
            "label": "Active rides",
            "value": str(active_rides_count),
            "trendText": "Driving or joined",
            "trendUp": True,
        },
        {
            "id": "pending-requests",
            "label": "Pending requests",
            "value": str(pending_requests_count),
            "trendText": "Awaiting decision",
            "trendUp": pending_requests_count > 0,
        },
        {
            "id": "completed-trips",
            "label": "Completed trips",
            "value": str(completed_trips_count),
            "trendText": "Successfully finished",
            "trendUp": True,
        },
        {
            "id": "cost-savings",
            "label": "Community savings",
            "value": f"${savings_value:,}",
            "trendText": "Estimated value saved",
            "trendUp": True,
        },
    ]


def get_upcoming_rides(db: Session, user_id: int, limit: int = 5) -> List[dict]:
    owned_rides = db.query(Ride).options(joinedload(Ride.vehicle)).filter(
        Ride.owner_id == user_id,
        Ride.status == "upcoming"
    ).all()

    joined_requests = db.query(RideRequest).options(
        joinedload(RideRequest.ride).joinedload(Ride.vehicle)
    ).filter(
        RideRequest.ride_requester_id == user_id,
        RideRequest.status == ACCEPTED_STATUS
    ).all()

    joined_rides = [req.ride for req in joined_requests if req.ride and req.ride.status == "upcoming"]

    all_rides_map = {ride.uuid: ride for ride in (owned_rides + joined_rides)}
    sorted_rides = sorted(all_rides_map.values(), key=lambda r: r.depart_time)[:limit]

    results = []
    for ride in sorted_rides:
        depart = ride.depart_time
        end = ride.end_time
        vehicle = ride.vehicle
        vehicle_str = vehicle.vehicle_plate if vehicle else "N/A"
        if vehicle and vehicle.vehicle_model:
            vehicle_str += f" ({vehicle.vehicle_model})"

        results.append({
            "id": ride.uuid,
            "route": f"{ride.town_starting} -> {ride.town_ending}",
            "startTown": ride.town_starting,
            "endTown": ride.town_ending,
            "startTime": depart.strftime("%I:%M %p") if depart else "",
            "etaTime": end.strftime("%I:%M %p") if end else "",
            "seatsAvailable": get_available_seats(ride),
            "vehicleNumber": vehicle_str,
        })
    return results


def get_dashboard_ride_requests(db: Session, user_id: int, limit: int = 5) -> List[dict]:
    requests, _ = get_all_user_requests(user_id=user_id, db=db, skip=0, limit=limit)

    status_map = {
        "Accepted": "approved",
        "Pending": "pending",
        "Rejected": "rejected",
        "Cancelled": "cancelled"
    }

    results = []
    for req in requests:
        requester = req.ride_requester
        p_name = f"{requester.first_name} {requester.last_name}" if requester else "Unknown Passenger"
        ride = req.ride
        route_str = f"{ride.town_starting} -> {ride.town_ending}" if ride else ""
        mapped_status = status_map.get(req.status, req.status.lower())
        is_owner = bool(ride and ride.owner_id == user_id)
        viewer_role = "owner" if is_owner else "requester"
        req_type = "incoming" if is_owner else "outgoing"

        results.append({
            "id": req.uuid,
            "passengerName": p_name,
            "seatsRequested": req.seats,
            "pickup": req.pickup,
            "dropOff": req.stop,
            "route": route_str,
            "status": mapped_status,
            "viewerRole": viewer_role,
            "type": req_type,
        })
    return results


def get_dashboard_activity(db: Session, user_id: int, limit: int = 5) -> List[dict]:
    user_rides = db.query(Ride.uuid).filter(Ride.owner_id == user_id).all()
    ride_uuids = [r[0] for r in user_rides]

    user_requests = db.query(RideRequest.uuid).filter(
        or_(
            RideRequest.ride_requester_id == user_id,
            RideRequest.ride_id.in_(
                db.query(Ride.id).filter(Ride.owner_id == user_id)
            )
        )
    ).all()
    req_uuids = [r[0] for r in user_requests]

    all_uuids = set(ride_uuids + req_uuids)

    query = db.query(AuditLog).options(
        joinedload(AuditLog.actor)
    )

    if all_uuids:
        query = query.filter(
            or_(
                AuditLog.actor_id == user_id,
                AuditLog.entity_uuid.in_(list(all_uuids))
            )
        )
    else:
        query = query.filter(AuditLog.actor_id == user_id)

    logs = query.order_by(AuditLog.created_at.desc()).limit(limit).all()

    results = []
    for log in logs:
        actor_name = f"{log.actor.first_name} {log.actor.last_name}" if log.actor else "System"

        summary = "Activity update"
        detail = f"Action: {log.action}"

        changes_dict = {}
        if log.changes:
            try:
                changes_dict = json.loads(log.changes)
            except Exception:
                pass

        if log.entity_type == "ride":
            if log.action == "created":
                summary = "New ride created"
                detail = f"{actor_name} posted a new ride."
            elif log.action == "updated":
                summary = "Ride details updated"
                detail = f"{actor_name} modified ride details."
            else:
                summary = f"Ride {log.action}"
                detail = f"Ride updated by {actor_name}."
        elif log.entity_type == "ride_request":
            if log.action == "created":
                summary = "New ride request"
                detail = f"{actor_name} requested a seat."
            elif log.action == "updated":
                summary = "Request updated"
                detail = f"{actor_name} updated request details."
            elif log.action == "status_changed":
                new_status = changes_dict.get("status", {}).get("to", "")
                if new_status == "Accepted":
                    summary = "Ride request approved"
                    detail = f"{actor_name} approved the ride request."
                elif new_status == "Rejected":
                    summary = "Ride request rejected"
                    detail = f"{actor_name} rejected the ride request."
                else:
                    summary = "Request status changed"
                    detail = f"{actor_name} updated request status to {new_status}."

        results.append({
            "id": f"act-{log.id}",
            "summary": summary,
            "detail": detail,
            "timestamp": format_relative_time(log.created_at),
        })

    return results
