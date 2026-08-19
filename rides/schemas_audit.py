from datetime import datetime
from typing import Optional, Any, Dict
from pydantic import BaseModel, ConfigDict


class AuditLogSchema(BaseModel):
    id: int
    entity_type: str
    entity_uuid: str
    action: str
    changes: Optional[Dict[str, Any]] = None
    actor_name: Optional[str] = None
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)
