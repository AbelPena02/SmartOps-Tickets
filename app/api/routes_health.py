from fastapi import APIRouter

router = APIRouter()

@router.get("/health")
def health_check():
    """
    Health check endpoint to verify API status.
    """
    return {"status": "ok", "message": "SmartOps Tickets API is running"}
