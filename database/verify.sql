-- Run after the development seed. Fails the command on a missing invariant.
\set ON_ERROR_STOP on
SELECT postgis_full_version();
DO $$
BEGIN
    IF (SELECT count(*) FROM study_areas WHERE area_type='province'
        AND name IN ('Lai Châu','Điện Biên','Sơn La','Yên Bái')) <> 4
        OR (SELECT count(*) FROM alert_rainfall_records WHERE alert_id=-1) <> 2
        OR (SELECT count(*) FROM gis_layer_study_areas WHERE layer_id=-1) <> 4 THEN
        RAISE EXCEPTION 'Seed relationships are incomplete';
    END IF;
    IF (SELECT count(*) FROM geometry_columns WHERE f_table_schema='public'
        AND f_table_name IN ('study_areas','landslide_events') AND srid=32648) <> 2 THEN
        RAISE EXCEPTION 'Incorrect geometry SRID';
    END IF;
END $$;
