from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.core.config import settings

engine = create_engine(
    settings.connection_url,
    pool_pre_ping=True,
    connect_args={
        "connect_timeout": 4,
        "options": f"-c timezone=UTC -c statement_timeout={settings.db_command_timeout_seconds * 1000}",
    },
)
SessionLocal = sessionmaker(engine)
