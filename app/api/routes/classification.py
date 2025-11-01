from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.core.db import get_db
from app.models.ticket import Ticket

router = APIRouter(prefix="/analytics", tags=["Analytics"])

@router.get("/summary")
async def get_ticket_summary(db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Ticket))
    tickets = result.scalars().all()

    summary = {"by_classification": {}, "by_priority": {}}

    for ticket in tickets:
        cls = getattr(ticket, "classification", "unknown")
        summary["by_classification"][cls] = summary["by_classification"].get(cls, 0) + 1
        summary["by_priority"][ticket.priority] = summary["by_priority"].get(ticket.priority, 0) + 1

    return summary
