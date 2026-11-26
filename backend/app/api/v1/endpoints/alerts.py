from typing import Annotated

from fastapi import APIRouter, Query

from app.api.dependencies import Database, ResourceId
from app.repositories import catalog
from app.schemas.catalog import AlertFilter, AlertOut, AlertDetail, Result
from app.services.catalog import alert_detail

router = APIRouter(prefix="/alerts", tags=["Alerts"])


@router.get("", response_model=Result[list[AlertOut]])
def list_alerts(db: Database, filters: Annotated[AlertFilter, Query()]):
    """List alerts matching the supplied filters."""
    return {"data": catalog.alerts(db, filters)}


@router.get("/{alert_id}", response_model=Result[AlertDetail], responses={404: {"description": "Resource not found"}})
def get_alert(db: Database, alert_id: ResourceId):
    """Return alerts details for one identifier."""
    return {"data": alert_detail(db, alert_id)}
