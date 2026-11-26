from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.models import Alert
from app.repositories.catalog import alert_rainfall
from app.schemas.catalog import AlertDetail, AlertOut


def get_resource(db: Session, model, resource_id: int):
    row = db.get(model, resource_id)
    if row is None:
        raise HTTPException(404, detail={
            "code": "RESOURCE_NOT_FOUND", "message": "The requested resource was not found."
        })
    return row


def alert_detail(db: Session, alert_id: int) -> AlertDetail:
    row = get_resource(db, Alert, alert_id)
    return AlertDetail(
        **AlertOut.model_validate(row).model_dump(),
        trigger_reason=row.trigger_reason,
        rainfall_records=alert_rainfall(db, alert_id),
    )
