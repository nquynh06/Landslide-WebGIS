from sqlalchemy import DateTime, cast, func, select
from sqlalchemy.orm import Session, defer

from app.models import (
    Alert, AlertRainfallRecord, GisLayer, GisLayerStudyArea,
    LandslideEvent, RainfallRecord, StudyArea, SusceptibilityMap,
)
from app.schemas.catalog import (
    AlertFilter, AreaFilter, EventFilter, LayerFilter, MapFilter, Page,
    RainfallFilter, TimeFilter,
)


def page_rows(db: Session, query, filters: Page):
    start = (filters.page - 1) * filters.page_size
    return db.scalars(query.offset(start).limit(filters.page_size)).all()


def filter_time(query, filters: TimeFilter, area_column, time_column):
    if filters.study_area_id is not None:
        query = query.where(area_column == filters.study_area_id)
    if filters.start_date is not None:
        query = query.where(time_column >= filters.start_date)
    if filters.end_date is not None:
        query = query.where(time_column < filters.end_date)
    return query


def study_areas(db: Session, filters: AreaFilter):
    query = select(StudyArea).options(defer(StudyArea.geom)).order_by(StudyArea.id)
    if filters.area_type is not None:
        query = query.where(StudyArea.area_type == filters.area_type)
    return page_rows(db, query, filters)


def layers(db: Session, filters: LayerFilter):
    query = select(GisLayer).order_by(GisLayer.id)
    if filters.study_area_id is not None:
        query = query.join(GisLayerStudyArea, GisLayerStudyArea.layer_id == GisLayer.id).where(
            GisLayerStudyArea.study_area_id == filters.study_area_id
        )
    if filters.layer_type is not None:
        query = query.where(GisLayer.layer_type == filters.layer_type)
    if filters.processing_status is not None:
        query = query.where(GisLayer.processing_status == filters.processing_status)
    return page_rows(db, query, filters)


def maps(db: Session, filters: MapFilter):
    query = select(SusceptibilityMap).order_by(SusceptibilityMap.id)
    if filters.study_area_id is not None:
        query = query.where(SusceptibilityMap.study_area_id == filters.study_area_id)
    if filters.status is not None:
        query = query.where(SusceptibilityMap.status == filters.status)
    return page_rows(db, query, filters)


def events(db: Session, filters: EventFilter):
    # A DATE represents midnight UTC, independent of the DB/session timezone.
    midnight_utc = func.timezone("UTC", cast(LandslideEvent.event_date, DateTime()))
    query = filter_time(select(LandslideEvent).options(defer(LandslideEvent.geom)),
                        filters, LandslideEvent.study_area_id, midnight_utc)
    if filters.event_type is not None:
        query = query.where(LandslideEvent.event_type == filters.event_type)
    return page_rows(db, query.order_by(LandslideEvent.event_date.desc().nulls_last(), LandslideEvent.id), filters)


def rainfall(db: Session, filters: RainfallFilter):
    query = filter_time(select(RainfallRecord), filters, RainfallRecord.study_area_id, RainfallRecord.observed_at)
    if filters.data_type is not None:
        query = query.where(RainfallRecord.data_type == filters.data_type)
    return page_rows(db, query.order_by(RainfallRecord.observed_at.desc(), RainfallRecord.id), filters)


def alerts(db: Session, filters: AlertFilter):
    query = filter_time(select(Alert), filters, Alert.study_area_id, Alert.issued_at)
    if filters.alert_level is not None:
        query = query.where(Alert.alert_level == filters.alert_level)
    if filters.status is not None:
        query = query.where(Alert.status == filters.status)
    return page_rows(db, query.order_by(Alert.issued_at.desc(), Alert.id), filters)


def alert_rainfall(db: Session, alert_id: int):
    query = (select(RainfallRecord)
             .join(AlertRainfallRecord, AlertRainfallRecord.rainfall_record_id == RainfallRecord.id)
             .where(AlertRainfallRecord.alert_id == alert_id)
             .order_by(RainfallRecord.observed_at.desc(), RainfallRecord.id))
    return db.scalars(query).all()
