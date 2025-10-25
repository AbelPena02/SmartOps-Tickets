from fastapi import FastAPI
from app.api.routes_health import router as health_router
from app.api.routes_tickets import router as tickets_router
from app.api.routes.classification import router as analytics_router
from app.core.logging_config import setup_logging
from app.core.db import init_db
import asyncio
import logging

setup_logging()
logger = logging.getLogger(__name__)

app = FastAPI(
    title="SmartOps Tickets API",
    version="0.1.0",
    description="AI-powered incident and ticket management system for DevOps teams."
)
 
# Routers
app.include_router(health_router)
app.include_router(tickets_router)
app.include_router(analytics_router)

@app.on_event("startup")
async def startup_event():
    await init_db()
    logger.info("Database initialized successfully")

@app.get("/", tags=["Root"])
async def root():
    logger.info("Root endpoint accessed")
    return {"message": "Welcome to SmartOps Tickets API"}
