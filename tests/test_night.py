import pytest
from collections import Counter
from src.secret_hitler.state import get_players_info, get_sh_game_phase
from src.secret_hitler.night import divvy_roles
from src.handlers.utils.lobby import get_lobby_status, get_lobby_by_code, join_lobby
from src.handlers.utils.game import start_game
from src.handlers.utils.users import create_user


async def _generate_users(lobby_code, prefix='tim', num_to_gen=4):
  users = []
  for x in range(num_to_gen):
    # Admin user is created in fixture
    u = await create_user(prefix+str(x), 'sess-'+prefix+str(x))
    users.append(u)
  for user in users:
    await join_lobby(lobby_code, user[0])


@pytest.mark.asyncio
async def test_night_phase_5_player(lobby_code):
  game = await get_lobby_by_code(lobby_code)
  await _generate_users(lobby_code)

  await start_game(game.id)
  r = await get_lobby_status(game.id)
  assert r == 'in_progress'

  r = await get_sh_game_phase(game.id)
  assert r == 'night'

  await divvy_roles(game.id)

  players = await get_players_info(game.id)
  assert len(players) == 5

  for player in players:
    roles = await get_players_info(game.id, player.get('user_id'))
    cur_user = [r for r in roles if r['user_id'] == player.get('user_id')][0]
    counts = Counter([r['display_role'] for r in roles])
    if cur_user['display_role'] == 'hitler':
      assert counts['fascist'] == 1
      assert counts['hitler'] == 1
      assert counts['liberal'] == 3
    elif cur_user['display_role'] == 'fascist':
      assert counts['fascist'] == 1
      assert counts['hitler'] == 1
      assert counts['liberal'] == 3
    else:
      assert counts['liberal'] == 5


@pytest.mark.asyncio
async def test_night_phase_6_player(lobby_code):
  game = await get_lobby_by_code(lobby_code)
  await _generate_users(lobby_code, prefix='dan6', num_to_gen=5)

  await start_game(game.id)
  r = await get_lobby_status(game.id)
  assert r == 'in_progress'

  r = await get_sh_game_phase(game.id)
  assert r == 'night'

  await divvy_roles(game.id)

  players = await get_players_info(game.id)
  assert len(players) == 6

  for player in players:
    roles = await get_players_info(game.id, player.get('user_id'))
    cur_user = [r for r in roles if r['user_id'] == player.get('user_id')][0]
    counts = Counter([r['display_role'] for r in roles])
    if cur_user['display_role'] == 'hitler':
      assert counts['fascist'] == 1
      assert counts['hitler'] == 1
      assert counts['liberal'] == 4
    elif cur_user['display_role'] == 'fascist':
      assert counts['fascist'] == 1
      assert counts['hitler'] == 1
      assert counts['liberal'] == 4
    else:
      assert counts['liberal'] == 6


@pytest.mark.asyncio
async def test_night_phase_7_player(lobby_code):
  game = await get_lobby_by_code(lobby_code)
  await _generate_users(lobby_code, prefix='dan7', num_to_gen=6)

  await start_game(game.id)
  r = await get_lobby_status(game.id)
  assert r == 'in_progress'

  r = await get_sh_game_phase(game.id)
  assert r == 'night'

  await divvy_roles(game.id)

  players = await get_players_info(game.id)
  assert len(players) == 7

  for player in players:
    roles = await get_players_info(game.id, player.get('user_id'))
    cur_user = [r for r in roles if r['user_id'] == player.get('user_id')][0]
    counts = Counter([r['display_role'] for r in roles])
    if cur_user['display_role'] == 'hitler':
      assert counts['hitler'] == 1
      assert counts['liberal'] == 6
    elif cur_user['display_role'] == 'fascist':
      assert counts['fascist'] == 2
      assert counts['hitler'] == 1
      assert counts['liberal'] == 4
    else:
      assert counts['liberal'] == 7


@pytest.mark.asyncio
async def test_night_phase_8_player(lobby_code):
  game = await get_lobby_by_code(lobby_code)
  await _generate_users(lobby_code, prefix='dan8', num_to_gen=7)

  await start_game(game.id)
  r = await get_lobby_status(game.id)
  assert r == 'in_progress'

  r = await get_sh_game_phase(game.id)
  assert r == 'night'

  await divvy_roles(game.id)

  players = await get_players_info(game.id)
  assert len(players) == 8

  for player in players:
    roles = await get_players_info(game.id, player.get('user_id'))
    cur_user = [r for r in roles if r['user_id'] == player.get('user_id')][0]
    counts = Counter([r['display_role'] for r in roles])
    if cur_user['display_role'] == 'hitler':
      assert counts['hitler'] == 1
      assert counts['liberal'] == 7
    elif cur_user['display_role'] == 'fascist':
      assert counts['fascist'] == 2
      assert counts['hitler'] == 1
      assert counts['liberal'] == 5
    else:
      assert counts['liberal'] == 8


@pytest.mark.asyncio
async def test_night_phase_9_player(lobby_code):
  game = await get_lobby_by_code(lobby_code)
  await _generate_users(lobby_code, prefix='dan9', num_to_gen=8)

  await start_game(game.id)
  r = await get_lobby_status(game.id)
  assert r == 'in_progress'

  r = await get_sh_game_phase(game.id)
  assert r == 'night'

  await divvy_roles(game.id)

  players = await get_players_info(game.id)
  assert len(players) == 9

  for player in players:
    roles = await get_players_info(game.id, player.get('user_id'))
    cur_user = [r for r in roles if r['user_id'] == player.get('user_id')][0]
    counts = Counter([r['display_role'] for r in roles])
    if cur_user['display_role'] == 'hitler':
      assert counts['hitler'] == 1
      assert counts['liberal'] == 8
    elif cur_user['display_role'] == 'fascist':
      assert counts['fascist'] == 3
      assert counts['hitler'] == 1
      assert counts['liberal'] == 5
    else:
      assert counts['liberal'] == 9


@pytest.mark.asyncio
async def test_night_phase_10_player(lobby_code):
  game = await get_lobby_by_code(lobby_code)
  await _generate_users(lobby_code, prefix='dan10', num_to_gen=9)

  await start_game(game.id)
  r = await get_lobby_status(game.id)
  assert r == 'in_progress'

  r = await get_sh_game_phase(game.id)
  assert r == 'night'

  await divvy_roles(game.id)

  players = await get_players_info(game.id)
  assert len(players) == 10

  for player in players:
    roles = await get_players_info(game.id, player.get('user_id'))
    cur_user = [r for r in roles if r['user_id'] == player.get('user_id')][0]
    counts = Counter([r['display_role'] for r in roles])
    if cur_user['display_role'] == 'hitler':
      assert counts['hitler'] == 1
      assert counts['liberal'] == 9
    elif cur_user['display_role'] == 'fascist':
      assert counts['fascist'] == 3
      assert counts['hitler'] == 1
      assert counts['liberal'] == 6
    else:
      assert counts['liberal'] == 10
