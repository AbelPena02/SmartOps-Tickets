from fastapi import FastAPI
from app.api.routes_health import router as health_router

app = FastAPI(title="SmartOps Tickets API", version="0.1.0")

app.include_router(health_router)

@app.get("/")
def root():
    return {"message": "Welcome to SmartOps Tickets API"}
