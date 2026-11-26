from typing import Annotated

from fastapi import APIRouter, Query

from app.api.dependencies import Database, ResourceId
from app.models import StudyArea
from app.repositories import catalog
from app.schemas.catalog import AreaFilter, StudyAreaOut, Result
from app.services.catalog import get_resource

router = APIRouter(prefix="/study-areas", tags=["Study areas"])


@router.get("", response_model=Result[list[StudyAreaOut]])
def list_study_areas(db: Database, filters: Annotated[AreaFilter, Query()]):
    """List study areas matching the supplied filters."""
    return {"data": catalog.study_areas(db, filters)}


@router.get("/{study_area_id}", response_model=Result[StudyAreaOut], responses={404: {"description": "Resource not found"}})
def get_study_area(db: Database, study_area_id: ResourceId):
    """Return study areas details for one identifier."""
    return {"data": get_resource(db, StudyArea, study_area_id)}
