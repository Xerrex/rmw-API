"""User access management: listing users and changing their role."""
from typing import List, Optional
from sqlalchemy.orm import Session
from db.models import User
from db.audit import log_action
from .schemas import VALID_ROLES


def list_users(db: Session, skip: int = 0, limit: int = 50) -> List[User]:
    return db.query(User).order_by(User.created_at.desc()).offset(skip).limit(limit).all()


def get_user_by_uuid(db: Session, user_uuid: str) -> Optional[User]:
    return db.query(User).filter(User.uuid == user_uuid).first()


def update_user_role(db: Session, user: User, new_role: str, actor_id: int) -> User:
    old_role = user.role
    user.role = new_role
    db.add(user)
    db.commit()
    db.refresh(user)

    log_action(
        db=db,
        entity_type="user",
        entity_uuid=user.uuid,
        action="role_changed",
        actor_id=actor_id,
        changes={"role": {"from": old_role, "to": new_role}},
    )
    return user
