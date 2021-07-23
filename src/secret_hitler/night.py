import random
import uuid

from src import db
from src.handlers.utils.lobby import get_lobby_members
from src.utils.context import get_context


async def divvy_roles(lobby_id):
  ctx = get_context()
  lobby = await get_lobby_members(lobby_id)
  cur_players = [x.user_id for x in lobby]
  roles = {}
  num_of_players = len(lobby)
  if num_of_players in (5, 6):
    num_of_fasc = 1
  else:
    num_of_fasc = num_of_players // 3

  for _ in range(num_of_fasc):
    p = random.choice(cur_players)
    roles.update({
      p: 'fascist'
    })
    cur_players.remove(p)

  hitler = random.choice(cur_players)
  roles.update({
    hitler: 'hitler'
  })
  cur_players.remove(hitler)
  random.shuffle(lobby)
  _values = [{
    'id': str(uuid.uuid4()),
    'lobby_id': lobby_id,
    'user_id': lobby.user_id,
    'play_order': idx,
    'role': roles.get(lobby.user_id, 'liberal')
  } for idx, lobby in list(enumerate(lobby))]
  await ctx.db.query(db.sh_roles.insert().values(_values))
