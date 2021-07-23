import random
import uuid

from src import db
from src.handlers.utils.users import list_users
from src.secret_hitler.elections import get_election_cycle, create_new_election, get_next_president, get_ineligible_players
from src.utils.context import get_context


async def get_sh_state(lobby_id):
  election = await get_election_cycle(lobby_id)
  if election.stage in ('policy_enacted', 'election_cycle_complete'):
    next_president_id = await get_next_president(lobby_id, election.president_id)
    election = await create_new_election(lobby_id, next_president_id)
  ineligible = await get_ineligible_players(lobby_id)
  return {
    'stage': election.stage,
    'president_id': election.president_id,
    'chancellor_id': election.chancellor_id,
    'chancellor_decided': election.chancellor_decided,
    'term_accepted': election.term_accepted,
    'drawn_policies': election.drawn_policies,
    'accepted_policy': election.accepted_policy,
    'president_burried': election.president_burried,
    'chancellor_burried': election.chancellor_burried,
    'ineligible': ineligible,
  }


async def get_players_info(lobby_id, user_id=None):
  ctx = get_context()
  query = db.sh_roles\
      .select()\
      .where(db.sh_roles.c.lobby_id == lobby_id)\
      .order_by(db.sh_roles.c.play_order.asc())
  results = await ctx.db.query(query)
  records = results.all()
  returns = []
  num_of_players = len(records)
  cur_user = None
  if user_id:
    cur_user = [r for r in records if r['user_id'] == user_id][0]

  users = await list_users(lobby_id)
  usernames = {user.id: user.username for user in users}

  for record in records:
    display_role = None
    if user_id:
      display_role = 'liberal'
      if cur_user.role == 'hitler' and num_of_players in (5, 6) and record.role in ('fascist', 'hitler'):
        display_role = record.role
      elif cur_user.role == 'fascist' and record.role in ('fascist', 'hitler'):
          display_role = record.role
      elif cur_user.role == 'hitler' and record.user_id == cur_user.user_id:
          display_role = record.role

    returns.append({
      'play_order': record.play_order,
      'user_id': record.user_id,
      'username': usernames.get(record.user_id, 'Unknown'),
      'display_role': display_role
    })

  return returns


async def new_sh_game(lobby_id):
  ctx = get_context()
  policies = ['liberal'] * 6 + ['fascist'] * 11
  random.shuffle(policies)
  _values = {
    'id': str(uuid.uuid4()),
    'lobby_id': lobby_id,
    'phase': 'night',
    'policies': policies
  }
  await ctx.db.query(db.sh_game_state.insert().values(_values))


async def get_sh_game_phase(lobby_id):
  ctx = get_context()
  r = await ctx.db.query(db.sh_game_state.select().where(db.sh_game_state.c.lobby_id == lobby_id))
  return r.one().phase


async def get_sh_game_state(lobby_id):
  ctx = get_context()
  r = await ctx.db.query(
    db.sh_game_state.select().where(db.sh_game_state.c.lobby_id == lobby_id))
  return r.one().id
