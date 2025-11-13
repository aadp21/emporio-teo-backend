#env.py
from logging.config import fileConfig
from sqlalchemy import engine_from_config, pool
from alembic import context

# 1) primero obtenemos el config de Alembic
config = context.config

# 2) ahora sí podemos importar nuestra config de FastAPI
from app.core.config import settings

# 3) y recién aquí le decimos a Alembic que use la URL de nuestra app
config.set_main_option("sqlalchemy.url", settings.DATABASE_URL)

# 4) logging (esto ya venía)
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# 5) importar la Base de SQLAlchemy donde están tus modelos
from app.db.base import Base
target_metadata = Base.metadata


def run_migrations_offline() -> None:
    """Run migrations in 'offline' mode."""
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
    """Run migrations in 'online' mode."""
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
