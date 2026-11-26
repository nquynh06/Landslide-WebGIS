-- Development only. Negative IDs are reserved for synthetic fixtures.
BEGIN;
INSERT INTO study_areas (name, area_type) VALUES
  ('Lai Châu', 'province'), ('Điện Biên', 'province'),
  ('Sơn La', 'province'), ('Yên Bái', 'province'),
  ('Tây Bắc (4 tỉnh)', 'study_region')
ON CONFLICT (area_type, name) DO NOTHING;

INSERT INTO data_sources (id, name, provider, notes)
VALUES (-1, 'Development sample', 'Landslide-WebGIS', 'Synthetic fixtures for API development only.')
ON CONFLICT (id) DO NOTHING;

INSERT INTO gis_layers (id, source_id, layer_name, layer_type, file_format, crs, resolution_m, processing_status, description)
VALUES (-1, -1, 'Sample DEM', 'raster', 'GeoTIFF', 'EPSG:32648', 250, 'draft', 'Development sample only.')
ON CONFLICT (id) DO NOTHING;
INSERT INTO gis_layer_study_areas (layer_id, study_area_id)
SELECT -1, id FROM study_areas WHERE area_type = 'province' AND name IN ('Lai Châu', 'Điện Biên', 'Sơn La', 'Yên Bái')
ON CONFLICT DO NOTHING;

INSERT INTO susceptibility_maps (id, study_area_id, map_name, version, method, crs, resolution_m, status, notes)
SELECT -1, id, 'Sample susceptibility map', 'dev-1', 'Weighted Overlay', 'EPSG:32648', 250, 'draft', 'Development sample only.'
FROM study_areas WHERE area_type = 'study_region' AND name = 'Tây Bắc (4 tỉnh)'
ON CONFLICT (id) DO NOTHING;
INSERT INTO landslide_events (id, study_area_id, source_id, location_name, event_type, description, confidence)
SELECT -1, id, -1, 'Sample location', 'landslide', 'Synthetic development event.', 'unverified'
FROM study_areas WHERE area_type = 'province' AND name = 'Lai Châu'
ON CONFLICT (id) DO NOTHING;

INSERT INTO rainfall_records (id, study_area_id, source_id, location_name, rainfall_mm, period_hours, data_type, observed_at, retrieved_at)
SELECT r.id, a.id, -1, 'Sample location', r.mm, 24, r.kind, '2026-01-01T00:00:00Z', '2026-01-01T00:15:00Z'
FROM study_areas a CROSS JOIN (VALUES (-1, 25.5, 'observation'), (-2, 0, 'forecast')) AS r(id, mm, kind)
WHERE a.area_type = 'province' AND a.name = 'Lai Châu'
ON CONFLICT (id) DO NOTHING;

INSERT INTO alerts (id, study_area_id, susceptibility_map_id, alert_level, title, message, trigger_reason, issued_at, status)
SELECT -1, id, -1, 'sample', 'Sample warning', 'Development test data.', 'Synthetic fixture for testing linked rainfall records.', '2026-01-01T01:00:00Z', 'active'
FROM study_areas WHERE area_type = 'province' AND name = 'Lai Châu'
ON CONFLICT (id) DO NOTHING;
INSERT INTO alert_rainfall_records (alert_id, rainfall_record_id) VALUES (-1, -1), (-1, -2)
ON CONFLICT DO NOTHING;
COMMIT;
