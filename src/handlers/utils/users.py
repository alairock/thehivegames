from uuid import uuid4

from sqlalchemy import literal_column, select
import enum
from src import db
from src.utils.context import get_context


class Status(enum.Enum):
  ACTIVE = 'active'
  INACTIVE = 'inactive'


async def list_users(lobby_id):
  ctx = get_context()
  sql = select([db.users, db.lobby_users]).select_from(db.lobby_users).where(db.lobby_users.c.lobby_id == lobby_id).join(db.users)
  r = await ctx.db.query(sql)
  return r.all()


async def change_username(user_id, username):
  ctx = get_context()
  _user = {'username': username}
  r = await ctx.db.query(
    db.users.update()
      .values(_user)
      .where(db.users.c.id == user_id)
      .returning(literal_column('*')))
  return r.one()


async def create_user(username):
  ctx = get_context()
  _user = {'id': str(uuid4()), 'username': username, 'status': Status.ACTIVE.value}
  r = await ctx.db.query(db.users.insert().values(_user).returning(literal_column('*')))
  return r.one()


async def mark_inactive(user_id):
  ctx = get_context()
  _user = {'user_id': user_id}
  _update = {'status': Status.INACTIVE.value}
  await ctx.db.query(db.users.update().values(_update)
                     .where(db.users.c.id == user_id))


async def mark_active(user_id):
  ctx = get_context()
  _user = {'user_id': user_id}
  _update = {'status': Status.ACTIVE.value}
  await ctx.db.query(db.users.update().values(_update)
                     .where(db.users.c.id == user_id))
