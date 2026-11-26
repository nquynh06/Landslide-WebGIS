from fastapi import APIRouter
from sqlalchemy import text

from app.api.dependencies import Database
from app.schemas.catalog import Health

router = APIRouter(tags=["Health"])


@router.get("/health", response_model=Health, responses={503: {"description": "Database unavailable"}})
def health(db: Database):
    """Check the API and its PostgreSQL connection."""
    db.execute(text("SELECT 1"))
    return Health(status="ok", database="connected")
