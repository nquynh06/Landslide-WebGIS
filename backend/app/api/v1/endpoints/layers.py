from typing import Annotated

from fastapi import APIRouter, Query

from app.api.dependencies import Database, ResourceId
from app.models import GisLayer
from app.repositories import catalog
from app.schemas.catalog import LayerFilter, LayerOut, Result
from app.services.catalog import get_resource

router = APIRouter(prefix="/layers", tags=["GIS layers"])


@router.get("", response_model=Result[list[LayerOut]])
def list_layers(db: Database, filters: Annotated[LayerFilter, Query()]):
    """List gis layers matching the supplied filters."""
    return {"data": catalog.layers(db, filters)}


@router.get("/{layer_id}", response_model=Result[LayerOut], responses={404: {"description": "Resource not found"}})
def get_gis_layer(db: Database, layer_id: ResourceId):
    """Return gis layers details for one identifier."""
    return {"data": get_resource(db, GisLayer, layer_id)}
