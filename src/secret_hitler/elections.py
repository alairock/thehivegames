import uuid
import typing
from sqlalchemy import literal_column
from collections import Counter
from src import db
from src.utils.context import get_context


async def get_election_cycle(lobby_id):
  ctx = get_context()
  results = await ctx.db.query(
    db.sh_elections.select()
      .where(db.sh_elections.c.lobby_id == lobby_id)
      .order_by(db.sh_elections.c.created_ts.desc()))

  election = results.one_or_none()
  if not election:
    # This is the first election
    r = await ctx.db.query(
      db.sh_roles.select()
      .where(db.sh_roles.c.lobby_id == lobby_id)
      .where(db.sh_roles.c.play_order == 0))
    president_id = r.one().user_id
    election = await create_new_election(lobby_id, president_id)
  return election


async def get_next_president(lobby_id, current_president_id):
  ctx = get_context()
  users = await ctx.db.query(
    db.sh_roles.select()
      .where(db.sh_roles.c.lobby_id == lobby_id))
  users = users.fetchall()
  next_idx = [user for user in users if user.user_id == current_president_id][0].play_order + 1
  if next_idx > len(users):
    next_idx = 0
  return [user for user in users if user.play_order == next_idx][0].user_id


async def create_new_election(lobby_id, president_id):
  ctx = get_context()
  _values = {
    'id': str(uuid.uuid4()),
    'lobby_id': lobby_id,
    'stage': 'nominating_chancellor',
    'president_id': president_id
  }
  results = await ctx.db.query(
    db.sh_elections.insert().values(_values)
      .returning(literal_column('*')))
  return results.one()


async def _update_election(lobby_id, election_id, values: dict):
  ctx = get_context()
  await ctx.db.query(
    db.sh_elections.update().values(values)
    .where(db.sh_elections.c.id == election_id)
    .where(db.sh_elections.c.lobby_id == lobby_id))


async def nominate_chancellor(lobby_id, election_id, chancellor_id):
  await _update_election(lobby_id, election_id, {'chancellor_id': chancellor_id, 'stage': 'confirming_chancellor'})


async def confirm_chancellor(lobby_id, election_id):
  await _update_election(lobby_id, election_id, {'chancellor_decided': True, 'stage': 'holding_election'})


async def cast_vote(lobby_id, election_id, civilian_id, vote: typing.Literal['ja', 'nein']):
  ctx = get_context()
  await create_new_vote(lobby_id, election_id, civilian_id, vote)
  cast_votes = await get_votes(lobby_id, election_id)
  results = await ctx.db.query(
    db.sh_roles.select()
      .where(db.sh_roles.c.lobby_id == lobby_id)
      .order_by(db.sh_roles.c.play_order.asc()))
  players = results.all()
  if len(cast_votes) == len(players):
    await _update_election(lobby_id, election_id, {'stage': 'election_complete'})


async def get_election_results(lobby_id, election_id):
  votes = await get_votes(lobby_id, election_id)
  counts = Counter([x.vote for x in votes])
  jas = counts.get('ja', 0)
  neins = counts.get('nein', 0)
  passes = True
  if neins >= jas:
    passes = False
  return passes


async def mark_results(lobby_id, election_id, passes: bool):
  stage = 'failed'
  if passes:
    stage = 'legislative_session'
  await _update_election(lobby_id, election_id, {'term_accepted': passes, 'stage': stage})


async def president_burry(lobby_id, election_id, policy: typing.Literal['fascist', 'liberal']):
  await _update_election(lobby_id, election_id, {'president_burried': policy, 'stage': 'chancellor_policy'})


async def chancellor_burry(lobby_id, election_id, policy: typing.Literal['fascist', 'liberal']):
  # No stage, since we will accept the policy at the same time
  await _update_election(lobby_id, election_id, {'chancellor_burried': policy})


async def get_ineligible_players(lobby_id):
  ctx = get_context()
  r = await ctx.db.query(
    db.sh_elections.select()
      .where(db.sh_elections.c.term_accepted.is_(True))
      .where(db.sh_elections.c.lobby_id == lobby_id)
      .order_by(db.sh_elections.c.created_ts.desc()))
  x = r.one_or_none()
  if x:
    return [x.president_id, x.chancellor_id]
  return []


async def create_new_vote(game_id, election_id, civilian_id, vote: typing.Literal['ja', 'nein']):
  ctx = get_context()
  _values = {
    'id': str(uuid.uuid4()),
    'game_id': game_id,
    'election_id': election_id,
    'civilian_id': civilian_id,
    'vote': vote
  }
  await ctx.db.query(db.sh_votes.insert().values(_values))
  return _values['id']


async def get_votes(game_id, election_id):
  ctx = get_context()
  results = await ctx.db.query(
    db.sh_votes.select()
    .where(db.sh_votes.c.game_id == game_id)
    .where(db.sh_votes.c.election_id == election_id))
  return results.all()
