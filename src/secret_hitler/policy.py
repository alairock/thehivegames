import typing

from src import db
from src.secret_hitler.elections import president_burry, chancellor_burry, _update_election
from src.utils.context import get_context


async def draw_policies(lobby_id, election_id):
  ctx = get_context()
  query = db.sh_game_state.select().where(db.sh_game_state.c.lobby_id == lobby_id)
  state = await ctx.db.query(query)
  x = state.one()
  drawn = []
  for _ in range(3):
    drawn.append(x.policies.pop())
  await save_drawn_policies(lobby_id, election_id, drawn)
  return drawn


async def handle_president_policy(lobby_id, election_id, discard):
  # TODO: Ensure the policy type was in the drawn policies #security
  await president_burry(lobby_id, election_id, discard)


async def handle_chancellor_policy(lobby_id, election_id, discard, approve):
  # TODO: Ensure the policy type was in the drawn policies #security
  # And also not the one that the president burried
  await chancellor_burry(lobby_id, election_id, discard)
  await accept_policy(lobby_id, election_id, approve)


async def accept_policy(lobby_id, election_id, policy: typing.Literal['fascist', 'liberal']):
  stage = 'policy_enacted'
  # TODO Check fascist policies, to see if we need to be on a different stage
  await _update_election(lobby_id, election_id, {'accepted_policy': policy, 'stage': stage})


async def save_drawn_policies(lobby_id, election_id, policies):
  await _update_election(lobby_id, election_id, {'drawn_policies': policies})


async def get_chancellor_policies(lobby_id, election_id):
  ctx = get_context()
  r = await ctx.db.query(
    db.sh_elections.select()
      .where(db.sh_elections.c.id == election_id)
      .where(db.sh_elections.c.lobby_id == lobby_id))
  x = r.one()
  x.drawn_policies.remove(x.president_burried)
  return x.drawn_policies
