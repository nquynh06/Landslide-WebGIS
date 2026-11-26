from pathlib import Path

from pydantic import Field, SecretStr
from pydantic_settings import BaseSettings, SettingsConfigDict
from sqlalchemy.engine import URL, make_url

BACKEND_ROOT = Path(__file__).resolve().parents[2]


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=BACKEND_ROOT / ".env", extra="ignore")

    app_name: str = "Landslide-WebGIS API"
    app_env: str = "development"
    debug: bool = False
    api_v1_prefix: str = "/api/v1"
    db_host: str = "localhost"
    db_port: int = Field(default=5432, ge=1, le=65535)
    db_name: str = "landslide_webgis"
    db_user: str = "landslide_user"
    db_password: SecretStr | None = None
    db_command_timeout_seconds: int = Field(default=30, ge=0, le=2147483)
    database_url: SecretStr | None = None
    migration_database_url: SecretStr | None = None
    test_database_url: SecretStr | None = None
    gis_data_root: str = ""
    map_service_base_url: str = ""
    rainfall_provider: str = ""
    rainfall_api_key: SecretStr = SecretStr("")

    @property
    def connection_url(self) -> URL:
        if self.database_url is not None:
            return make_url(self.database_url.get_secret_value())
        return URL.create(
            "postgresql+psycopg", username=self.db_user,
            password=self.db_password.get_secret_value() if self.db_password else None,
            host=self.db_host, port=self.db_port, database=self.db_name,
        )


settings = Settings()
