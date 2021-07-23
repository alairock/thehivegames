import random
import uuid
import enum

from sqlalchemy import literal_column, select
from sqlalchemy.engine import CursorResult
from src import db
from src.game_confs import GAME_CONFIGS
from src.utils.context import get_context
from src.utils.exceptions import GameNotFoundError


class Status(enum.Enum):
   LOBBY = 'lobby'
   INPROGRESS = 'in_progress'
   GAMEOVER = 'gameover'


async def create_lobby_code():
  ctx = get_context()
  while True:
    lobby_code = ''.join((random.choice('0123456789abcdghjklmnpqrstvwxyz') for _ in range(4))).upper()
    lc_exists = await lobby_code_exists(lobby_code)
    if lc_exists:
      break

  _lobby = {
    'id': str(uuid.uuid4()),
    'game': 'SH',
    'lobby_code': lobby_code,
    'max_players': 10,
    'status': Status.LOBBY.value
  }
  await ctx.db.query(db.lobby.insert().values(_lobby))
  return lobby_code


async def lobby_code_exists(lobby_code):
  ctx = get_context()
  r = await ctx.db.query(db.lobby.select()
                         .where(db.lobby.c.lobby_code == lobby_code)
                         .where(db.lobby.c.status != Status.GAMEOVER.value))
  return not bool(r.one_or_none())


async def join_lobby(lobby_code, user_id):
  lobby = await get_lobby_by_code(lobby_code)
  if not lobby:
    raise GameNotFoundError('Game not found.')
  size = await lobby_size(lobby.id)
  mp = lobby.max_players
  if size + 1 > mp:
    raise Exception('Too many players in this lobby.')
  ctx = get_context()
  _lobby = {'id': str(uuid.uuid4()), 'lobby_id': lobby.id, 'user_id': user_id}
  r = await ctx.db.query(db.lobby_users.insert().values(_lobby).returning(literal_column('*')))
  return r.one()


async def leave_lobby(lobby_code, user_id):
  ctx = get_context()
  lobby = await get_lobby_by_code(lobby_code)
  # TODO: If user is admin
  # TODO: Check if there is any other players in lobby

  # TODO: If there are no players in lobby, close game.

  # TODO: If there are other players in the lobby, transfer owner to another user in the lobby

  # TODO: If user is not an admin, just remove record. For now this is default action.

  r: CursorResult = await ctx.db.query(
    db.lobby_users.delete()
      .where(db.lobby_users.c.user_id == user_id)
      .where(db.lobby_users.c.lobby_id == lobby.id))


async def get_lobby_by_code(lobby_code):
  ctx = get_context()
  r: CursorResult = await ctx.db.query(db.lobby.select().where(db.lobby.c.lobby_code == lobby_code))
  return r.one_or_none()


async def change_lobby_status(lobby_id, status: Status):
  ctx = get_context()
  await ctx.db.query(db.lobby.update().values({'status': status.value}).where(db.lobby.c.id == lobby_id))


async def get_lobby_status(lobby_id):
  ctx = get_context()
  r: CursorResult = await ctx.db.query(db.lobby.select().where(db.lobby.c.id == lobby_id))
  return r.one().status


async def get_lobby_state(lobby_code):
  lobby = await get_lobby_by_code(lobby_code)
  if not lobby:
    raise GameNotFoundError('Game not found.')
  members = await get_lobby_members(lobby.id)
  _game = {
    'game': lobby.game,
    'status': lobby.status,
    'min_players': GAME_CONFIGS[lobby.game]['min_players'],
    'max_players': GAME_CONFIGS[lobby.game]['max_players']
  }
  _members = {'members': [{'id': member.id, 'username': member.username} for member in members]}
  if lobby.status != 'lobby':
  #   state = {}
  #   if lobby.game == 'SH':
  #     state = await get_sh_state(lobby.id)

    _game = {
      'game': lobby.game,
      'status': lobby.status,
      # 'state': state
    }
  return {'game': _game,
          **_members}


async def get_lobby_members(lobby_id):
  ctx = get_context()
  sql = select([db.users, db.lobby_users]).select_from(db.lobby_users).where(db.lobby_users.c.lobby_id == lobby_id).join(db.users)
  r = await ctx.db.query(sql)
  return r.all()


async def lobby_size(lobby_id):
  ctx = get_context()
  r: CursorResult = await ctx.db.query(db.lobby_users.select().where(db.lobby_users.c.lobby_id == lobby_id))
  return len(r.all())
