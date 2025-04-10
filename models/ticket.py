# src/models/ticket.py
from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class Ticket(BaseModel):
    id: str
    user_id: str
    user_name: str
    message: str
    created_at: datetime = datetime.now()
    status: str = "new"  # new, in_progress, resolved
    assigned_to: Optional[str] = None