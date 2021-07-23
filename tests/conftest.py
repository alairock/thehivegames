import asyncio
import random
import uuid

import pytest
from pytest import fixture
from sqlalchemy.ext.asyncio import create_async_engine

from src.utils.context import DBContextPool, db_context
from src.handlers.utils.lobby import create_lobby_code


@pytest.fixture(scope='session')
def event_loop():
    """Create an instance of the default event loop for each test case."""
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


@pytest.fixture(scope='session')
def ctx():
    engine = create_async_engine(
        "postgresql+asyncpg://postgres:password@localhost:5132/postgres", echo=True,
    )
    ctx = DBContextPool(engine)
    db_context.set(ctx)
    return ctx


@pytest.mark.asyncio
@fixture(autouse=True)
async def lobby_code(event_loop, ctx):
    uname = ''.join((random.choice('0123456789abcdghjklmnpqrstvwxyz') for i in range(6))).upper()
    return await create_lobby_code(str(uuid.uuid4()), uname)
