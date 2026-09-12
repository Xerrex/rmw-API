from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from auth.deps_auth import get_current_user
from auth.schemas import UserSchema
from auth.crud import update_user_password
from auth.handler_password import verify_password
from db.db_deps import get_db
from db.models import User
from .schemas import VehicleSchema, VehicleCreateSchema, ChangePasswordSchema
from .crud_vehicles import get_user_vehicles, create_user_vehicle, delete_user_vehicle


router = APIRouter()


@router.get("/me")
def my_details(current_user: UserSchema = Depends(get_current_user)):
    """My details
    
    Get details of the current logged in users.
    """
    return current_user


@router.get("/vehicles", response_model=List[VehicleSchema])
def list_vehicles(
    db: Session = Depends(get_db),
    current_user: UserSchema = Depends(get_current_user)
):
    """Get all vehicles owned by the current user."""
    return get_user_vehicles(db=db, user_id=current_user.id)


@router.post("/vehicles", response_model=VehicleSchema, status_code=status.HTTP_201_CREATED)
def add_vehicle(
    data: VehicleCreateSchema,
    db: Session = Depends(get_db),
    current_user: UserSchema = Depends(get_current_user)
):
    """Add a new vehicle for the current user."""
    return create_user_vehicle(db=db, user_id=current_user.id, data=data)


@router.delete("/vehicles/{vehicle_id}", status_code=status.HTTP_200_OK)
def remove_vehicle(
    vehicle_id: int,
    db: Session = Depends(get_db),
    current_user: UserSchema = Depends(get_current_user)
):
    """Delete a vehicle if no rides are associated with it."""
    delete_user_vehicle(db=db, user_id=current_user.id, vehicle_id=vehicle_id)
    return {"message": "Vehicle deleted successfully", "success": True}


@router.post("/change-password", status_code=status.HTTP_200_OK)
def change_password(
    data: ChangePasswordSchema,
    db: Session = Depends(get_db),
    current_user: UserSchema = Depends(get_current_user)
):
    """Change the current user's password after verifying the current password."""
    db_user = db.query(User).filter(User.id == current_user.id).first()
    if not db_user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")

    if not verify_password(data.current_password, db_user.password):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Current password provided is incorrect."
        )

    update_user_password(uuid=db_user.uuid, password=data.new_password, db=db)
    return {"message": "Password changed successfully", "success": True}