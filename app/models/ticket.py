from sqlalchemy import Column, Integer, String, Text, DateTime
from datetime import datetime
from app.core.db import Base

class Ticket(Base):
    __tablename__ = "tickets"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    description = Column(Text)
    classification = Column(String, default="general")
    priority = Column(String, default="medium")
    status = Column(String, default="open")
    created_at = Column(DateTime, default=datetime.utcnow)
