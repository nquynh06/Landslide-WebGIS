from typing import Annotated

from fastapi import APIRouter, Query

from app.api.dependencies import Database
from app.repositories import catalog
from app.schemas.catalog import RainfallFilter, RainfallOut, Result

router = APIRouter(prefix="/rainfall", tags=["Rainfall"])


@router.get("", response_model=Result[list[RainfallOut]])
def list_rainfall(db: Database, filters: Annotated[RainfallFilter, Query()]):
    """List rainfall matching the supplied filters."""
    return {"data": catalog.rainfall(db, filters)}
