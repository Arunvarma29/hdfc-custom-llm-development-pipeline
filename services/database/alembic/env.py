from logging.config import fileConfig

from alembic import context
from sqlalchemy import engine_from_config, pool

from services.database.app.config import settings
from services.database.app.base import Base

# Import all models that belong to the central database metadata.

from services.dataset_registry.app.models import Dataset  # noqa: F401
from services.data_preparation.app.models.preparation_job import PreparationJob  # noqa: F401
from services.data_preparation.app.models.prepared_artifact import (
    PreparedArtifact,
)  # noqa: F401


from services.data_preparation.app.models.preparation_quality_report import (
    PreparationQualityReport,
)  # noqa: F401




config = context.config

# Use the database URL from centralized settings.
config.set_main_option(
    "sqlalchemy.url",
    settings.database_url,
)

if config.config_file_name is not None:
    fileConfig(config.config_file_name)


# Alembic will compare the database against this metadata.
target_metadata = Base.metadata


def run_migrations_offline() -> None:
    """Run migrations in offline mode."""

    url = config.get_main_option("sqlalchemy.url")

    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online() -> None:
    """Run migrations in online mode."""

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


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()