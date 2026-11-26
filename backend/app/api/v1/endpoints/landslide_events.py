from typing import Annotated

from fastapi import APIRouter, Query

from app.api.dependencies import Database
from app.repositories import catalog
from app.schemas.catalog import EventFilter, EventOut, Result

router = APIRouter(prefix="/landslide-events", tags=["Landslide events"])


@router.get("", response_model=Result[list[EventOut]])
def list_events(db: Database, filters: Annotated[EventFilter, Query()]):
    """List landslide events matching the supplied filters."""
    return {"data": catalog.events(db, filters)}
