import pytest

from src.handlers.utils.lobby import get_lobby_status, get_lobby_by_code, join_lobby
from src.handlers.utils.game import start_game
from src.utils.lobby import join_lobby
from src.handlers.utils.users import create_user


@pytest.mark.asyncio
async def test_start_game_empty_lobby(lobby_code):
  game = await get_lobby_by_code(lobby_code)
  await start_game(game.id)
  r = await get_lobby_status(game.id)
  assert r == 'lobby'


@pytest.mark.asyncio
async def test_start_game(lobby_code):
  users = []
  game = await get_lobby_by_code(lobby_code)
  for x in range(3):
    # Admin user is created in fixture
    u = await create_user('tom-'+str(x), 'sess-'+str(x))
    users.append(u)
  for user in users:
    await join_lobby(lobby_code, user[0])

  # At this point we only have 4 players. Not enough to start
  # Check to make sure that starting the game doesn't
  await start_game(game.id)
  r = await get_lobby_status(game.id)
  assert r == 'lobby'

  # One more is joining...
  u = await create_user('LateTate', 'sess-99')
  await join_lobby(u[0], game.id)

  # Now we have enough. Start game should change status
  await start_game(game.id)
  r = await get_lobby_status(game.id)
  assert r == 'in_progress'
