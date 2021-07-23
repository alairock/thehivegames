from sqlalchemy import Table, Column, String, BOOLEAN, ForeignKey, Text, SMALLINT, Index
from sqlalchemy.dialects.postgresql import TIMESTAMP, JSONB
import sqlalchemy as sa

METADATA = sa.MetaData()

lobby = Table(
  'lobby', METADATA,
  Column('id', Text, primary_key=True),
  Column('lobby_code', String(6), nullable=False, index=True),
  Column('game', Text),
  Column('admin_id', ForeignKey('users.id'), nullable=True),  # Only user that can start the game
  Column('max_players', SMALLINT, default='10'),
  Column('status', String(32), nullable=False),
  Column('created_ts', TIMESTAMP, nullable=False, server_default=sa.text('NOW()')),
)

lobby_users = Table(
  'lobby_users', METADATA,
  Column('id', Text, primary_key=True),
  Column('lobby_id', ForeignKey('lobby.id'), nullable=False),
  Column('user_id', ForeignKey('users.id'), nullable=False),
  Column('created_ts', TIMESTAMP, server_default=sa.text('NOW()')),
)
Index('lobby_user_uniq', lobby_users.c.lobby_id, lobby_users.c.user_id, unique=True)


users = Table(
  'users', METADATA,
  Column('id', Text, primary_key=True),
  Column('username', Text, index=True),
  Column('passphrase', Text),
  Column('status', Text, nullable=False),
  Column('created_ts', TIMESTAMP, server_default=sa.text('NOW()')),
)
Index('username_passphrase_uniq', users.c.username, users.c.passphrase, unique=True)


# SECRET HITLER #
sh_game_state = Table(
  'sh_game_state', METADATA,
  Column('id', Text, primary_key=True),
  Column('lobby_id', ForeignKey('lobby.id'), nullable=False, index=True),
  Column('phase', Text),
  Column('policies', JSONB),
  Column('created_ts', TIMESTAMP, server_default=sa.text('NOW()')),
)

sh_roles = Table(
  'sh_roles', METADATA,
  Column('id', Text, primary_key=True),
  Column('lobby_id', ForeignKey('lobby.id'), nullable=False),
  Column('user_id', ForeignKey('users.id'), nullable=False),
  Column('play_order', SMALLINT, nullable=False),
  Column('role', Text)  # Hitler, Fascist, Liberal
)

sh_elections = Table(
  'sh_elections', METADATA,
  Column('id', Text, primary_key=True),
  Column('lobby_id', ForeignKey('lobby.id'), nullable=False),
  Column('stage', String, nullable=False),
  Column('president_id', ForeignKey('users.id'), nullable=False),
  Column('chancellor_id', ForeignKey('users.id'), nullable=True),
  Column('chancellor_decided', BOOLEAN, nullable=True),
  Column('term_accepted', BOOLEAN, nullable=True),
  Column('drawn_policies', JSONB, nullable=True),
  Column('accepted_policy', String, nullable=True),
  Column('president_burried', String, nullable=True),
  Column('chancellor_burried', String, nullable=True),
  Column('created_ts', TIMESTAMP, server_default=sa.text('NOW()')),
)

sh_votes = Table(
  'sh_votes', METADATA,
  Column('id', Text, primary_key=True),
  Column('lobby_id', ForeignKey('lobby.id'), nullable=False),
  Column('election_id', ForeignKey('sh_elections.id'), nullable=False),
  Column('civilian_id', ForeignKey('users.id'), nullable=False),
  Column('vote', Text, nullable=False),
  Column('created_ts', TIMESTAMP, server_default=sa.text('NOW()')),
)
