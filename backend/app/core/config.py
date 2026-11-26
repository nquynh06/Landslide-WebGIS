from pathlib import Path

from pydantic import SecretStr
from pydantic_settings import BaseSettings, SettingsConfigDict

BACKEND_ROOT = Path(__file__).resolve().parents[2]


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=BACKEND_ROOT / ".env", extra="ignore")

    app_name: str = "Landslide-WebGIS API"
    app_env: str = "development"
    api_v1_prefix: str = "/api/v1"
    database_url: SecretStr
    migration_database_url: SecretStr | None = None
    test_database_url: SecretStr | None = None
    gis_data_root: str = ""
    map_service_base_url: str = ""
    rainfall_provider: str = ""
    rainfall_api_key: SecretStr = SecretStr("")


settings = Settings()
