from src import db
from src.game_confs import GAME_CONFIGS
from src.handlers.utils.lobby import get_lobby_by_code, Status, lobby_size
from src.secret_hitler.state import new_sh_game
from src.secret_hitler.night import divvy_roles
from src.utils.context import get_context


async def start_game(lobby_code):
  ctx = get_context()
  lobby = await get_lobby_by_code(lobby_code)
  # Check if there are enough people in the lobby
  _lobby_size = await lobby_size(lobby.id)
  if _lobby_size >= GAME_CONFIGS[lobby.game]['min_players']:
    await ctx.db.query(
      db.lobby.update()
        .values({'status': Status.INPROGRESS.value})
        .where(db.lobby.c.id == lobby.id))
    await new_sh_game(lobby.id)
    await divvy_roles(lobby.id)


async def end_game(lobby_code):
  ctx = get_context()
  lobby = await get_lobby_by_code(lobby_code)
