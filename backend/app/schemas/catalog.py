from datetime import date, datetime
from typing import Annotated, Generic, Literal, TypeVar

from pydantic import AwareDatetime, BaseModel, ConfigDict, Field, model_validator

T = TypeVar("T")
FilterText = Annotated[str, Field(pattern=r"^[^\x00]*$")]
DatabaseId = Annotated[int, Field(ge=-(2**63), le=2**63 - 1)]


class Result(BaseModel, Generic[T]):
    data: T


class Health(BaseModel):
    status: str
    database: str


class Row(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int


class StudyAreaOut(Row):
    name: str
    area_type: str
    province_code: str | None


class LayerOut(Row):
    source_id: int
    layer_name: str
    layer_type: str
    file_format: str | None
    crs: str | None
    resolution_m: float | None
    processing_status: str
    description: str | None


class MapOut(Row):
    study_area_id: int
    map_name: str
    version: str
    method: str
    crs: str | None
    resolution_m: float | None
    status: str
    generated_at: datetime | None


class MapDetail(MapOut):
    score_description: str | None
    notes: str | None
    legend: None = Field(None, description="Draft maps have no finalized GIS legend.")


class EventOut(Row):
    study_area_id: int
    source_id: int | None
    event_date: date | None
    location_name: str | None
    event_type: str | None
    description: str | None
    confidence: str | None


class RainfallOut(Row):
    study_area_id: int | None
    source_id: int
    location_name: str | None
    latitude: float | None
    longitude: float | None
    rainfall_mm: float
    period_hours: int
    data_type: Literal["observation", "forecast"]
    observed_at: datetime
    retrieved_at: datetime


class AlertOut(Row):
    study_area_id: int
    susceptibility_map_id: int | None
    alert_level: str
    title: str
    message: str
    issued_at: datetime
    valid_until: datetime | None
    status: str


class AlertDetail(AlertOut):
    trigger_reason: str | None
    rainfall_records: list[RainfallOut]


class Page(BaseModel):
    page: int = Field(default=1, ge=1, le=2147483647)
    page_size: int = Field(default=20, ge=1, le=100)


class AreaFilter(Page):
    area_type: FilterText | None = None


class LayerFilter(Page):
    study_area_id: DatabaseId | None = None
    layer_type: FilterText | None = None
    processing_status: FilterText | None = None


class MapFilter(Page):
    study_area_id: DatabaseId | None = None
    status: FilterText | None = None


class TimeFilter(Page):
    study_area_id: DatabaseId | None = None
    start_date: AwareDatetime | None = None
    end_date: AwareDatetime | None = None

    @model_validator(mode="after")
    def validate_interval(self):
        if self.start_date and self.end_date and self.start_date >= self.end_date:
            raise ValueError("end_date must be later than start_date")
        return self


class EventFilter(TimeFilter):
    event_type: FilterText | None = None


class RainfallFilter(TimeFilter):
    data_type: Literal["observation", "forecast"] | None = None


class AlertFilter(TimeFilter):
    alert_level: FilterText | None = None
    status: Literal["active", "expired", "cancelled"] | None = None
