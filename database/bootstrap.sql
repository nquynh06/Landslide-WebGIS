-- Run as administrator in each new target database, before applying the schema.
\set ON_ERROR_STOP on
\getenv owner_password LANDSLIDE_OWNER_PASSWORD
\getenv app_password LANDSLIDE_APP_PASSWORD
SELECT format('CREATE ROLE landslide_owner LOGIN PASSWORD %L', :'owner_password')
WHERE NOT EXISTS (SELECT FROM pg_roles WHERE rolname = 'landslide_owner') \gexec
SELECT format('CREATE ROLE landslide_user LOGIN PASSWORD %L', :'app_password')
WHERE NOT EXISTS (SELECT FROM pg_roles WHERE rolname = 'landslide_user') \gexec

CREATE EXTENSION IF NOT EXISTS postgis;
GRANT USAGE, CREATE ON SCHEMA public TO landslide_owner;
GRANT USAGE ON SCHEMA public TO landslide_user;
