# API Specification — Landslide-WebGIS

## 1. Purpose

This document defines the REST API contract for the Landslide-WebGIS application.

The backend is responsible for:
- Providing study area information.
- Providing GIS layer metadata.
- Providing susceptibility map metadata.
- Providing historical landslide event information.
- Providing rainfall records.
- Providing warning and alert information.
- Supporting future integration with GIS map services.

The backend is developed using FastAPI and PostgreSQL/PostGIS.

## 2. General API Convention

### 2.1 Base URL

Development:

`http://localhost:8000`

API prefix:

`/api/v1`

Example:

`http://localhost:8000/api/v1/study-areas`

### 2.2 HTTP Methods

| Method | Purpose |
|---|---|
| GET | Retrieve data |
| POST | Create or submit data |
| PUT | Replace a resource |
| PATCH | Partially update a resource |
| DELETE | Delete a resource |

The initial implementation primarily uses GET endpoints. Administrative write operations can be added when authentication and authorization requirements are defined.

### 2.3 Response Format

Successful responses should return JSON.

Example:

```json
{
  "data": [],
  "message": "Request successful"
}
```

For a single resource:

```json
{
  "data": {
    "id": 1,
    "name": "Lai Chau"
  },
  "message": "Request successful"
}
```

For errors:

```json
{
  "detail": {
    "code": "RESOURCE_NOT_FOUND",
    "message": "The requested resource was not found."
  }
}
```

FastAPI's default validation error format may be retained initially, provided it is documented and used consistently.

### 2.4 Common Query Parameters

Where relevant, endpoints may support:

| Parameter | Type | Description |
|---|---|---|
| page | integer | Page number |
| page_size | integer | Number of records per page |
| study_area_id | integer | Filter by study area |
| start_date | datetime | Start of time range |
| end_date | datetime | End of time range |
| status | string | Filter by status |

Pagination defaults and maximum values should be configured centrally.

## 3. API Endpoints

### 3.1 Health Check

**GET `/api/v1/health`**

Purpose: Check whether the backend is running and whether the database connection is available.

Example response:

```json
{
  "status": "ok",
  "database": "connected"
}
```

The endpoint should return an appropriate HTTP error if a required dependency is unavailable. Do not expose credentials or internal connection strings.

### 3.2 Study Areas

**GET `/api/v1/study-areas`**

Purpose: Retrieve all study areas.

Optional query parameters:
- `area_type`
- `page`
- `page_size`

Example response:

```json
{
  "data": [
    {
      "id": 1,
      "name": "Lai Chau",
      "area_type": "province",
      "province_code": null
    },
    {
      "id": 2,
      "name": "Dien Bien",
      "area_type": "province",
      "province_code": null
    }
  ]
}
```

The initial study area consists of Lai Chau, Dien Bien, Son La and Yen Bai.

**GET `/api/v1/study-areas/{study_area_id}`**

Purpose: Retrieve one study area's details.

The response may include its boundary as GeoJSON when required by the frontend. Large geometries should not be returned unnecessarily in list responses.

### 3.3 GIS Layers

**GET `/api/v1/layers`**

Purpose: Retrieve metadata about available GIS layers.

Optional query parameters:
- `study_area_id`
- `layer_type`
- `processing_status`

Example response:

```json
{
  "data": [
    {
      "id": 1,
      "layer_name": "DEM",
      "layer_type": "raster",
      "file_format": "GeoTIFF",
      "crs": "EPSG:32648",
      "resolution_m": 250,
      "processing_status": "processed"
    }
  ]
}
```

The API returns metadata, not the complete raster file.

**GET `/api/v1/layers/{layer_id}`**

Purpose: Retrieve details of one GIS layer.

The API must not expose arbitrary server filesystem paths to public clients. If a layer needs to be displayed, the backend should provide a configured map-service URL or a controlled resource endpoint.

### 3.4 Susceptibility Maps

**GET `/api/v1/susceptibility-maps`**

Purpose: Retrieve available susceptibility map versions.

Optional query parameters:
- `study_area_id`
- `status`

Example response:

```json
{
  "data": [
    {
      "id": 1,
      "study_area_id": 1,
      "map_name": "Landslide Susceptibility Map",
      "version": "v1",
      "method": "Weighted Overlay",
      "crs": "EPSG:32648",
      "resolution_m": 250,
      "status": "draft",
      "generated_at": null
    }
  ]
}
```

**GET `/api/v1/susceptibility-maps/{map_id}`**

Purpose: Retrieve one map's metadata, legend and publication information.

The legend and score interpretation must come from the finalized GIS methodology. Do not invent class boundaries.

**GET `/api/v1/susceptibility-maps/{map_id}/map-info`**

Purpose: Retrieve the configured map display information.

The response may contain:
- Map service type.
- Layer identifier.
- Configured service URL.
- Display bounds.
- CRS.
- Legend information.

This endpoint should only return a URL that has been configured and made accessible by the deployment environment.

### 3.5 Landslide Events

**GET `/api/v1/landslide-events`**

Purpose: Retrieve historical landslide events.

Optional query parameters:
- `study_area_id`
- `start_date`
- `end_date`
- `event_type`
- `page`
- `page_size`

Example response:

```json
{
  "data": [
    {
      "id": 1,
      "study_area_id": 1,
      "event_date": null,
      "location_name": "Sample location",
      "event_type": "landslide",
      "description": "Sample record for development",
      "confidence": "unverified"
    }
  ]
}
```

A sample record must be clearly identified as test data. It must not be presented as a real historical landslide event.

Where spatial display is needed, the endpoint may support GeoJSON output or a separate GeoJSON endpoint.

### 3.6 Rainfall

**GET `/api/v1/rainfall`**

Purpose: Retrieve rainfall observations or forecast records.

Optional query parameters:
- `study_area_id`
- `data_type`
- `start_date`
- `end_date`
- `page`
- `page_size`

Example response:

```json
{
  "data": [
    {
      "id": 1,
      "study_area_id": 1,
      "location_name": "Sample location",
      "rainfall_mm": 25.5,
      "period_hours": 24,
      "data_type": "observation",
      "observed_at": "2026-01-01T00:00:00Z",
      "retrieved_at": "2026-01-01T00:15:00Z"
    }
  ]
}
```

The example is illustrative only.

The implementation must distinguish:
- Observation data.
- Forecast data.
- Rainfall accumulation period.
- Time when the data is valid.
- Time when the system retrieved the data.

The actual rainfall provider, temporal resolution, spatial coverage and units must be verified before production integration.

### 3.7 Alerts

**GET `/api/v1/alerts`**

Purpose: Retrieve warning records.

Optional query parameters:
- `study_area_id`
- `alert_level`
- `status`
- `start_date`
- `end_date`
- `page`
- `page_size`

Example response:

```json
{
  "data": [
    {
      "id": 1,
      "study_area_id": 1,
      "susceptibility_map_id": 1,
      "alert_level": "sample",
      "title": "Sample warning",
      "message": "This is development test data.",
      "issued_at": "2026-01-01T00:00:00Z",
      "valid_until": null,
      "status": "active"
    }
  ]
}
```

**GET `/api/v1/alerts/{alert_id}`**

Purpose: Retrieve detailed information about one alert, including its associated rainfall records and the conditions that triggered it.

Alert levels and trigger thresholds are TBD until the rainfall warning methodology is approved.

## 4. Future Administrative Endpoints

These endpoints are not required for the first backend milestone.

| Method | Endpoint | Purpose |
|---|---|---|
| POST | `/api/v1/rainfall/ingest` | Submit or import rainfall data |
| POST | `/api/v1/alerts/evaluate` | Evaluate warning conditions |
| POST | `/api/v1/alerts` | Create an alert |
| PATCH | `/api/v1/alerts/{id}` | Update alert status |
| POST | `/api/v1/susceptibility-maps` | Register a new map version |

These operations should be protected before being exposed beyond the development environment.

## 5. API Implementation Priorities

### Phase 1 — Backend Foundation

Implement:
1. `GET /api/v1/health`
2. `GET /api/v1/study-areas`
3. `GET /api/v1/layers`
4. `GET /api/v1/susceptibility-maps`
5. `GET /api/v1/landslide-events`
6. `GET /api/v1/rainfall`
7. `GET /api/v1/alerts`

Use seeded development data where real GIS data is not yet available.

### Phase 2 — GIS Integration

- Connect actual study area geometries.
- Register final GIS layers.
- Connect susceptibility map metadata.
- Configure the map service.
- Provide map display information to the frontend.
- Support spatial queries where required.

### Phase 3 — Rainfall and Warning

- Integrate the selected rainfall provider.
- Store normalized rainfall records.
- Implement documented warning rules.
- Create alert records.
- Test alert generation and expiration.

## 6. API Documentation and Testing

FastAPI should provide interactive API documentation through:
- `/docs`
- `/redoc`

Each endpoint should have:
- Clear description.
- Request and response schema.
- Query parameter validation.
- Appropriate HTTP status codes.
- Error handling.
- Automated tests.

## 7. Important Constraints

1. Do not invent rainfall values, warning thresholds or susceptibility class boundaries.
2. Do not expose private filesystem paths or API keys.
3. Do not return large raster files as JSON.
4. Do not treat sample records as real geographic observations.
5. Keep the API version prefix `/api/v1`.
6. Maintain consistent response schemas and datetime formats.
7. Document any changes to this API contract before frontend integration.