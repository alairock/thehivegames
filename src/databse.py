import os
from sqlalchemy.ext.asyncio import create_async_engine

from src.utils.context import DBContextPool

DB_HOST = os.getenv('DB_HOST', 'localhost')
DB_PORT = os.getenv('DB_PORT', '5132')

def async_setup(app):
  async def _setup():
    engine = create_async_engine(
          f"postgresql+asyncpg://postgres:password@{DB_HOST}:{DB_PORT}/postgres", echo=False,
      )
    app.state.pool = DBContextPool(engine)
    app.state.db_engine = engine
  return _setup
