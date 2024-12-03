from datetime import datetime, timezone
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from .db_setup import Base


class User(Base):
    """User
    """
    
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    first_name =  Column(String(20), nullable=False)
    last_name = Column(String(20), nullable=False)
    username = Column(String(20), nullable=False)
    email = Column(String(100), nullable=False, unique=True, index=True)
    password = Column(String, nullable=False)
   
    created_at = Column(DateTime(timezone=True), default=datetime.now(timezone.utc))
    updated_at = Column(DateTime(timezone=True), default=datetime.now(timezone.utc), onupdate=datetime.now(timezone.utc))
    
    rides = relationship("Ride", back_populates="owner", cascade="all, delete-orphan")

    ride_requests = relationship('RideRequest',  back_populates="ride_requester", cascade="all, delete-orphan")


    # TODO: Add Token generation and verification


class Ride(Base):
    """Ride
    """

    __tablename__ = "rides"

    id = Column(Integer, primary_key=True)
    vehicle_plate = Column(String(20), nullable=False)
    seats = Column(Integer, nullable=False)
    town_starting = Column(String(80), nullable=False)
    town_ending = Column(String(80), nullable=False)
    depart_time = Column(DateTime(timezone=True), nullable=False)
    end_time = Column(DateTime(timezone=True), nullable=False)

    created_at = Column(DateTime(timezone=True), default=datetime.now(timezone.utc))
    updated_at = Column(DateTime(timezone=True), default=datetime.now(timezone.utc), onupdate=datetime.now(timezone.utc))

    owner_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    owner = relationship("User", back_populates="rides") # Relationship: back reference to the user
   
    ride_requests = relationship("RideRequest", back_populates="ride", cascade="all, delete-orphan")


class RideRequest(Base):
    """Ride Request 
    """

    __tablename__ = "rideRequests"

    id = Column(Integer, primary_key=True)
    seats = Column(Integer, nullable=False, default=1)
    stop = Column(String(80), default='Ride Destination', nullable=False)
    status = Column(String(10), default='Pending', nullable=False) # Accepted/Rejected

    created_at = Column(DateTime(timezone=True), default=datetime.now(timezone.utc))
    updated_at = Column(DateTime(timezone=True), default=datetime.now(timezone.utc), onupdate=datetime.now(timezone.utc))

    ride_id = Column(Integer, ForeignKey("rides.id", ondelete="CASCADE"), nullable=False)
    ride = relationship("Ride", back_populates="ride_requests") # Relationship: back reference to the ride

    ride_requester_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    ride_requester = relationship("User", back_populates="ride_requests") # Relationship: back reference to the user

