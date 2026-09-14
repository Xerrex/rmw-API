"""Audit logging helpers for rides and ride requests.

Re-exports the shared implementation in db.audit so existing imports
(`from .audit import log_action`) inside the rides package keep working.
"""
from db.audit import log_action, diff_fields

__all__ = ["log_action", "diff_fields"]

