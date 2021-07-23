import sqlalchemy as sa
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import sessionmaker

from src.utils.context import get_context


async def query(q, single_row=False):
    ctx = get_context()
    if isinstance(q, str):
        q = sa.text(q)

    result = await ctx.db.query(q)
    if single_row:
        return result.first()
    return result


def transact():
    ctx = get_context()
    return ctx.db.transact()


def get_session():
    ctx = get_context()
    return sessionmaker(
        ctx.db.engine, expire_on_commit=False, class_=AsyncSession)()
