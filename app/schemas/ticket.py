from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class TicketBase(BaseModel):
    title: str
    description: Optional[str] = None
    priority: Optional[str] = "medium"
    status: Optional[str] = "open"

class TicketCreate(TicketBase):
    pass

class TicketUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    priority: Optional[str] = None
    status: Optional[str] = None

class TicketOut(TicketBase):
    id: int
    created_at: datetime

    model_config = {
        "from_attributes": True
    }
