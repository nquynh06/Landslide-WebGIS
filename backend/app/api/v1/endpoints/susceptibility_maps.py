from typing import Annotated

from fastapi import APIRouter, Query

from app.api.dependencies import Database, ResourceId
from app.models import SusceptibilityMap
from app.repositories import catalog
from app.schemas.catalog import MapFilter, MapOut, MapDetail, Result
from app.services.catalog import get_resource

router = APIRouter(prefix="/susceptibility-maps", tags=["Susceptibility maps"])


@router.get("", response_model=Result[list[MapOut]])
def list_maps(db: Database, filters: Annotated[MapFilter, Query()]):
    """List susceptibility maps matching the supplied filters."""
    return {"data": catalog.maps(db, filters)}


@router.get("/{map_id}", response_model=Result[MapDetail], responses={404: {"description": "Resource not found"}})
def get_susceptibility_map(db: Database, map_id: ResourceId):
    """Return susceptibility maps details for one identifier."""
    return {"data": get_resource(db, SusceptibilityMap, map_id)}
