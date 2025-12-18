
# # from __future__ import annotations

# # from logging.config import fileConfig
# # from typing import Any

# # from alembic import context
# # from sqlalchemy import engine_from_config, pool
# # from sqlalchemy.engine import Connection
# # from sqlalchemy.ext.asyncio import AsyncEngine

# # from app.core.config import get_settings
# # from app.core.db.base import Base
# # from app.core.models import *  # noqa: F401,F403


# from __future__ import annotations

# import sys
# from pathlib import Path
# from logging.config import fileConfig
# from typing import Any

# from alembic import context
# from sqlalchemy import engine_from_config, pool
# from sqlalchemy.engine import Connection
# from sqlalchemy.ext.asyncio import AsyncEngine

# # 👇 THIS FIXES "No module named app"
# ROOT_DIR = Path(__file__).resolve().parents[2]
# sys.path.append(str(ROOT_DIR))

# from app.core.config import get_settings
# from app.core.db.base import Base
# from app.core.models import * 


# config = context.config

# if config.config_file_name is not None:
#     fileConfig(config.config_file_name)

# target_metadata = Base.metadata


# def _get_database_url() -> str:
#     settings = get_settings()
#     return str(settings.alembic_database_url or settings.database_url)


# def run_migrations_offline() -> None:
#     """
#     Run migrations in 'offline' mode.
#     """

#     url = _get_database_url()
#     context.configure(
#         url=url,
#         target_metadata=target_metadata,
#         literal_binds=True,
#         dialect_opts={"paramstyle": "named"},
#     )

#     with context.begin_transaction():
#         context.run_migrations()


# def do_run_migrations(connection: Connection) -> None:
#     context.configure(connection=connection, target_metadata=target_metadata)

#     with context.begin_transaction():
#         context.run_migrations()


# async def run_migrations_online() -> None:
#     """
#     Run migrations in 'online' mode using an async engine.
#     """

#     configuration = config.get_section(config.config_ini_section) or {}
#     configuration["sqlalchemy.url"] = _get_database_url()

#     connectable = AsyncEngine(
#         engine_from_config(
#             configuration,
#             prefix="sqlalchemy.",
#             poolclass=pool.NullPool,
#             future=True,
#         )
#     )

#     async with connectable.connect() as connection:
#         await connection.run_sync(do_run_migrations)

#     await connectable.dispose()


# if context.is_offline_mode():
#     run_migrations_offline()
# else:
#     import asyncio

#     asyncio.run(run_migrations_online())



from __future__ import annotations

import sys
from pathlib import Path
from logging.config import fileConfig

from alembic import context
from sqlalchemy import pool
from sqlalchemy.engine import Connection
from sqlalchemy.ext.asyncio import async_engine_from_config

# 👇 Fix import path
ROOT_DIR = Path(__file__).resolve().parents[2]
sys.path.append(str(ROOT_DIR))

from app.core.config import get_settings
from app.core.db.base import Base
from app.core.models import *  # noqa

config = context.config

if config.config_file_name is not None:
    fileConfig(config.config_file_name)

target_metadata = Base.metadata



def get_database_url() -> str:
    settings = get_settings()
    return str(settings.alembic_database_url or settings.database_url)
    print("ALEMBIC DB URL =", url)


def run_migrations_offline() -> None:
    context.configure(
        url=get_database_url(),
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()


def do_run_migrations(connection: Connection) -> None:
    context.configure(
        connection=connection,
        target_metadata=target_metadata,
    )

    with context.begin_transaction():
        context.run_migrations()


async def run_migrations_online() -> None:
    configuration = config.get_section(config.config_ini_section) or {}
    configuration["sqlalchemy.url"] = get_database_url()

    connectable = async_engine_from_config(
        configuration,
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
        future=True,
    )

    async with connectable.connect() as connection:
        await connection.run_sync(do_run_migrations)

    await connectable.dispose()


if context.is_offline_mode():
    run_migrations_offline()
else:
    import asyncio
    asyncio.run(run_migrations_online())
