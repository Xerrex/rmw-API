from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from auth.deps_auth import require_management_access, require_admin
from auth.schemas import UserSchema
from db.db_deps import get_db
from .crud_analytics import get_analytics
from .crud_users import list_users, get_user_by_uuid, update_user_role
from .schemas import AnalyticsSchema, ManagedUserSchema, UpdateUserRoleSchema, VALID_ROLES

router = APIRouter()


@router.get("/analytics", response_model=AnalyticsSchema)
def get_management_analytics(
    db: Session = Depends(get_db),
    current_user: UserSchema = Depends(require_management_access),
):
    """Aggregate platform metrics for admins/staff."""
    return get_analytics(db=db)


@router.get("/users", response_model=List[ManagedUserSchema])
def get_users(
    skip: int = 0,
    limit: int = 50,
    db: Session = Depends(get_db),
    current_user: UserSchema = Depends(require_management_access),
):
    """List app users so admins/staff can review access levels."""
    return list_users(db=db, skip=skip, limit=limit)


@router.put("/users/{user_uuid}/role", response_model=ManagedUserSchema)
def set_user_role(
    user_uuid: str,
    data: UpdateUserRoleSchema,
    db: Session = Depends(get_db),
    current_user: UserSchema = Depends(require_admin),
):
    """Change a user's role. Only admins can grant/revoke management access."""
    if data.role not in VALID_ROLES:
        detail = f"Role must be one of: {VALID_ROLES}"
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=detail)

    user = get_user_by_uuid(db=db, user_uuid=user_uuid)
    if not user:
        detail = f"User with uuid: '{user_uuid}' does not exist."
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=detail)

    return update_user_role(db=db, user=user, new_role=data.role, actor_id=current_user.id)
