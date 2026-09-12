import uuid
from datetime import datetime, timezone
from typing import List, Optional
from sqlalchemy import Integer, String, DateTime, ForeignKey, Boolean
from sqlalchemy.orm import relationship, Mapped, mapped_column
from sqlalchemy.sql import func
from .db_setup import Base


class User(Base):
    """User
    """
    
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    uuid: Mapped[str] = mapped_column(String(36), unique=True, default=lambda: str(uuid.uuid4()))
    first_name: Mapped[str] = mapped_column(String(20), nullable=False)
    last_name: Mapped[str] = mapped_column(String(20), nullable=False)
    # username = Column(String(20), nullable=True) # TODO: consider adding later
    email: Mapped[str] = mapped_column(String(100), nullable=False, unique=True, index=True)
    password: Mapped[str] = mapped_column(String, nullable=False)

    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=datetime.now(timezone.utc))
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=datetime.now(timezone.utc), onupdate=datetime.now(timezone.utc))
    
    rides: Mapped[List["Ride"]] = relationship("Ride", back_populates="owner", cascade="all, delete-orphan")
    vehicles: Mapped[List["Vehicle"]] = relationship("Vehicle", back_populates="owner", cascade="all, delete-orphan")
    ride_requests: Mapped[List["RideRequest"]] = relationship('RideRequest',  back_populates="ride_requester", cascade="all, delete-orphan")
    refresh_tokens: Mapped[List["RefreshToken"]] = relationship("RefreshToken", back_populates="user", cascade="all, delete-orphan")


class RefreshToken(Base):
    __tablename__ = "refresh_tokens"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    user_uuid: Mapped[str] = mapped_column(String(36), ForeignKey("users.uuid", ondelete="CASCADE"), nullable=False)
    token: Mapped[str] = mapped_column(String(255), unique=True, index=True, nullable=False)
    expires_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    is_revoked: Mapped[bool] = mapped_column(Boolean, default=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    
    user: Mapped[Optional["User"]] = relationship("User", back_populates="refresh_tokens")


class Vehicle(Base):
    """Vehicle owned by a user
    """

    __tablename__ = "vehicles"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    uuid: Mapped[str] = mapped_column(String(36), unique=True, default=lambda: str(uuid.uuid4()))
    vehicle_plate: Mapped[str] = mapped_column(String(20), nullable=False)
    vehicle_model: Mapped[str] = mapped_column(String(80), nullable=False)
    seats: Mapped[int] = mapped_column(Integer, nullable=False, default=4)

    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=datetime.now(timezone.utc))
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=datetime.now(timezone.utc), onupdate=datetime.now(timezone.utc))

    owner_id: Mapped[int] = mapped_column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    owner: Mapped[Optional["User"]] = relationship("User", back_populates="vehicles")
    rides: Mapped[List["Ride"]] = relationship("Ride", back_populates="vehicle")


class Ride(Base):
    """Ride
    """

    __tablename__ = "rides"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    uuid: Mapped[str] = mapped_column(String(36), unique=True, default=lambda: str(uuid.uuid4()))
    vehicle_plate: Mapped[str] = mapped_column(String(20), nullable=False)
    vehicle_model: Mapped[str] = mapped_column(String(80), nullable=False, server_default="")
    seats: Mapped[int] = mapped_column(Integer, nullable=False)
    town_starting: Mapped[str] = mapped_column(String(80), nullable=False)
    town_ending: Mapped[str] = mapped_column(String(80), nullable=False)
    depart_time: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    end_time: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    status: Mapped[str] = mapped_column(String(15), nullable=False, default="upcoming", server_default="upcoming")

    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=datetime.now(timezone.utc))
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=datetime.now(timezone.utc), onupdate=datetime.now(timezone.utc))

    vehicle_id: Mapped[Optional[int]] = mapped_column(Integer, ForeignKey("vehicles.id", ondelete="RESTRICT"), nullable=True)
    vehicle: Mapped[Optional["Vehicle"]] = relationship("Vehicle", back_populates="rides")

    owner_id: Mapped[int] = mapped_column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    owner: Mapped[Optional["User"]] = relationship("User", back_populates="rides") # Relationship: back reference to the user
    ride_requests: Mapped[List["RideRequest"]] = relationship("RideRequest", back_populates="ride", cascade="all, delete-orphan")


class RideRequest(Base):
    """Ride Request 
    """

    __tablename__ = "rideRequests"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    uuid: Mapped[str] = mapped_column(String(36), unique=True, default=lambda: str(uuid.uuid4()))
    seats: Mapped[int] = mapped_column(Integer, nullable=False, default=1)
    pickup: Mapped[str] = mapped_column(String(80), default='Ride Start', nullable=False)
    stop: Mapped[str] = mapped_column(String(80), default='Ride Destination', nullable=False)
    status: Mapped[str] = mapped_column(String(10), default='Pending', nullable=False) # Accepted/Rejected
    # JSON-encoded list of names occupying the extra seats (seats - 1), owner-only visibility
    passenger_names: Mapped[Optional[str]] = mapped_column(String, nullable=True)

    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=datetime.now(timezone.utc))
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=datetime.now(timezone.utc), onupdate=datetime.now(timezone.utc))

    ride_id: Mapped[int] = mapped_column(Integer, ForeignKey("rides.id", ondelete="CASCADE"), nullable=False)
    ride: Mapped[Optional["Ride"]] = relationship("Ride", back_populates="ride_requests") # Relationship: back reference to the ride

    ride_requester_id: Mapped[int] = mapped_column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    ride_requester: Mapped[Optional["User"]] = relationship("User", back_populates="ride_requests") # Relationship: back reference to the user


class AuditLog(Base):
    """Audit trail of changes made to rides and ride requests.
    """

    __tablename__ = "audit_logs"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    entity_type: Mapped[str] = mapped_column(String(20), nullable=False)  # "ride" | "ride_request"
    entity_uuid: Mapped[str] = mapped_column(String(36), nullable=False, index=True)
    action: Mapped[str] = mapped_column(String(40), nullable=False)  # e.g. "created", "updated", "status_changed"
    changes: Mapped[Optional[str]] = mapped_column(String, nullable=True)  # JSON-encoded {field: {"from": x, "to": y}}
    actor_id: Mapped[Optional[int]] = mapped_column(Integer, ForeignKey("users.id", ondelete="SET NULL"), nullable=True)

    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=datetime.now(timezone.utc))

    actor: Mapped[Optional["User"]] = relationship("User")

