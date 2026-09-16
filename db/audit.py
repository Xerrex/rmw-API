"""Shared audit logging helpers.

Centralizes writing to the audit_logs table so every mutation across the
app (rides, ride requests, user management, CLI actions, etc.) leaves a
traceable record of who changed what and when.
"""
import json
from typing import Optional
from sqlalchemy.orm import Session
from db.models import AuditLog


def log_action(db: Session, entity_type: str, entity_uuid: str, action: str,
                actor_id: Optional[int] = None, changes: Optional[dict] = None):
    """Persist an audit log entry.

    Args:
        db (Session): Database session.
        entity_type (str): kind of entity affected e.g. "ride", "ride_request", "user".
        entity_uuid (str): uuid of the affected entity.
        action (str): short description of what happened e.g. "created", "updated".
        actor_id (int, optional): id of the user who performed the action.
        changes (dict, optional): mapping of field -> {"from": old, "to": new}.
    """
    entry = AuditLog(
        entity_type=entity_type,
        entity_uuid=entity_uuid,
        action=action,
        actor_id=actor_id,
        changes=json.dumps(changes, default=str) if changes else None,
    )
    db.add(entry)
    db.commit()
    return entry


def diff_fields(before: dict, after: dict) -> dict:
    """Build a {field: {from, to}} map for values that changed."""
    changes = {}
    for key, new_value in after.items():
        old_value = before.get(key)
        if old_value != new_value:
            changes[key] = {"from": old_value, "to": new_value}
    return changes
