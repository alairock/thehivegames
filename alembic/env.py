import os
from logging.config import fileConfig
import os
import sys
from pathlib import Path

from sqlalchemy import pool, create_engine

from alembic import context

# this is the Alembic Config object, which provides
# access to the values within the .ini file in use.
from src import db

config = context.config

# Interpret the config file for Python logging.
# This line sets up loggers basically.
fileConfig(config.config_file_name)

# add your model's MetaData object here
sys.path.insert(0, str(Path(__file__).parent))
target_metadata = db.METADATA

# other values from the config, defined by the needs of env.py,
# can be acquired:
# my_important_option = config.get_main_option("my_important_option")
# ... etc.

DB_HOST = os.getenv('DB_HOST', 'localhost')
DB_PORT = os.getenv('DB_PORT', '5132')

def get_database_url():
    POSTGRES_URL = DB_HOST
    POSTGRES_USERNAME = os.getenv('SQL_USERNAME', 'postgres')
    POSTGRES_PASSWORD = os.getenv('SQL_PASSWORD', 'password')
    POSTGRES_DB_NAME = os.getenv('SQL_NAME', 'postgres')
    POSTGRES_DB_PORT = DB_PORT

    url = 'postgresql://{user}:{password}@{host}:{port}/{db}'.format(
      user=POSTGRES_USERNAME,
      password=POSTGRES_PASSWORD,
      host=POSTGRES_URL,
      db=POSTGRES_DB_NAME,
      port=POSTGRES_DB_PORT
    )
    return url


def run_migrations():
    db_url = get_database_url()
    connectable = create_engine(db_url, poolclass=pool.NullPool)

    with connectable.connect() as connection:
        context.configure(
            connection=connection,
            target_metadata=target_metadata,
            compare_type=True
        )

        with context.begin_transaction():
            context.run_migrations()


run_migrations()
