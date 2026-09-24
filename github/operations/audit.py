"""Audit records for repository operations."""
from datetime import datetime, timezone
def record(action,target,status,details=None):
    return {"timestamp":datetime.now(timezone.utc).isoformat(),"action":action,"target":target,"status":status,"details":details or {}}
