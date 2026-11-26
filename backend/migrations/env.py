from alembic import context
from sqlalchemy import create_engine, make_url, pool, text

from app.core.config import settings
from app.models import Base


url = (make_url(settings.migration_database_url.get_secret_value())
       if settings.migration_database_url else settings.connection_url)
options = dict(target_metadata=Base.metadata, compare_type=True)

if context.is_offline_mode():
    context.configure(url=url, literal_binds=True, **options)
    with context.begin_transaction():
        context.run_migrations()
else:
    engine = create_engine(
        url, poolclass=pool.NullPool,
        connect_args={"options": "-c search_path=public"},
    )
    with engine.connect() as connection:
        extension_tables = set(connection.scalars(text("""
            SELECT c.relname FROM pg_class c
            JOIN pg_depend d ON d.objid = c.oid AND d.classid = 'pg_class'::regclass
            WHERE d.deptype = 'e' AND d.refclassid = 'pg_extension'::regclass
              AND c.relnamespace = current_schema()::regnamespace
        """)))
        connection.commit()
        def include_name(name, type_, parent_names):
            return type_ != "table" or name not in extension_tables

        context.configure(connection=connection, include_name=include_name, **options)
        with context.begin_transaction():
            context.run_migrations()
