from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.core.db import get_db
from app.models.ticket import Ticket
from app.schemas.ticket import TicketCreate, TicketOut, TicketUpdate
from app.nlp.classifier import TicketClassifier
from app.nlp.priority_scorer import PriorityScorer

router = APIRouter(prefix="/tickets", tags=["Tickets"])

classifier = TicketClassifier()
priority_scorer = PriorityScorer()

@router.post("/", response_model=TicketOut)
async def create_ticket(ticket: TicketCreate, db: AsyncSession = Depends(get_db)):
    classification = classifier.classify(ticket.description)
    priority = priority_scorer.score(ticket.description)

    new_ticket = Ticket(
        title=ticket.title,
        description=ticket.description,
        classification=classification,
        priority=priority,
        status="open"
    )

    db.add(new_ticket)
    await db.commit()
    await db.refresh(new_ticket)

    return new_ticket

@router.get("/", response_model=list[TicketOut])
async def list_tickets(db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Ticket))
    return result.scalars().all()

@router.get("/{ticket_id}", response_model=TicketOut)
async def get_ticket(ticket_id: int, db: AsyncSession = Depends(get_db)):
    ticket = await db.get(Ticket, ticket_id)
    if not ticket:
        raise HTTPException(status_code=404, detail="Ticket not found")
    return ticket

@router.put("/{ticket_id}", response_model=TicketOut)
async def update_ticket(ticket_id: int, update: TicketUpdate, db: AsyncSession = Depends(get_db)):
    ticket = await db.get(Ticket, ticket_id)
    if not ticket:
        raise HTTPException(status_code=404, detail="Ticket not found")

    for key, value in update.dict(exclude_unset=True).items():
        setattr(ticket, key, value)

    if "description" in update.dict(exclude_unset=True):
        ticket.classification = classifier.classify(ticket.description)
        ticket.priority = priority_scorer.score(ticket.description)

    await db.commit()
    await db.refresh(ticket)
    return ticket

@router.delete("/{ticket_id}")
async def delete_ticket(ticket_id: int, db: AsyncSession = Depends(get_db)):
    ticket = await db.get(Ticket, ticket_id)
    if not ticket:
        raise HTTPException(status_code=404, detail="Ticket not found")
    await db.delete(ticket)
    await db.commit()
    return {"message": f"Ticket {ticket_id} deleted successfully"}

@router.post("/analyze")
async def analyze_ticket(data: dict):
    description = data.get("description")
    if not description:
        raise HTTPException(status_code=400, detail="Description missing")

    classification = classifier.classify(description)
    priority = priority_scorer.score(description)

    return {
        "description": description,
        "predicted_classification": classification,
        "predicted_priority": priority
    }

