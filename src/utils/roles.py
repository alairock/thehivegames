import typing

from src import db
from src.utils.context import get_db

Role = typing.Union[typing.Literal['hitler'], typing.Literal['fascist'], typing.Literal['liberal']]


async def assign_role(user_id, role: Role):
  q = get_db()
  _lobby = {'user_id': user_id, 'role': role}
  await q.query(db.sh_roles.insert().values(_lobby))
