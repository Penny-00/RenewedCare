from logging.config import fileConfig
import os
import sys

from sqlalchemy import engine_from_config
from sqlalchemy import pool
from alembic import context
import geoalchemy2

# --- Alembic Config ---
config = context.config

# --- Logging Setup ---
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# --- Add project root to sys.path ---
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

# --- Import your SQLAlchemy Base and DB URL ---
from database.db_connection import Base, DATABASE_URL
from database.models import disease_dim, disease_indicator, mortality_statistic, outbreak_reports, geo_unit, health_facilities


# --- Let Alembic know which metadata to use ---
target_metadata = Base.metadata

# --- Inject your DB URL dynamically ---
config.set_main_option("sqlalchemy.url", DATABASE_URL)


# --- Run migrations offline ---
def run_migrations_offline():
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
        user_module_prefix="geoalchemy2."
    )

    with context.begin_transaction():
        context.run_migrations()


# --- Run migrations online ---
def run_migrations_online():
    connectable = engine_from_config(
        config.get_section(config.config_ini_section, {}),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    with connectable.connect() as connection:
        context.configure(
            connection=connection,
            target_metadata=target_metadata,
        )

        with context.begin_transaction():
            context.run_migrations()


# --- Choose mode automatically ---
if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
