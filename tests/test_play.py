import pytest

from src.secret_hitler.elections import nominate_chancellor, confirm_chancellor, cast_vote, get_election_results, \
  mark_results
from src.secret_hitler.state import get_sh_state, get_players_info
from src.secret_hitler.policy import draw_policies, handle_president_policy, handle_chancellor_policy, \
  get_chancellor_policies
from src.secret_hitler.night import divvy_roles
from src.handlers.utils.lobby import get_lobby_by_code, join_lobby
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
async def test_round_1(lobby_code):
  game = await get_lobby_by_code(lobby_code)
  await _generate_users(lobby_code, prefix='test-us')
  await start_game(game.id)
  await divvy_roles(game.id)
  players = await get_players_info(game.id)
  election = await get_sh_state(game.id)
  assert election.stage == 'nominating_chancellor'

  await nominate_chancellor(game.id, election.id, players[3].get('user_id'))
  election = await get_sh_state(game.id)
  assert election.stage == 'confirming_chancellor'

  await confirm_chancellor(game.id, election.id)
  election = await get_sh_state(game.id)
  assert election.stage == 'holding_election'

  for player in players:
    await cast_vote(game.id, election.id, player.get('user_id'), 'ja')
  election = await get_sh_state(game.id)
  assert election.stage == 'election_complete'

  results = await get_election_results(game.id, election.id)
  await mark_results(game.id, election.id, results)
  election = await get_sh_state(game.id)
  assert election.stage == 'legislative_session'

  drawn = await draw_policies(game.id, election.id)
  president_burry = drawn[1]
  await handle_president_policy(game.id, election.id, president_burry)
  chancellor_policies = await get_chancellor_policies(game.id, election.id)
  chancellor_burry = chancellor_policies[1]
  chancellor_approved = chancellor_policies[0]
  await handle_chancellor_policy(game.id, election.id, chancellor_burry, chancellor_approved)
  election = await get_sh_state(game.id)

  assert election.stage == 'nominating_chancellor'
