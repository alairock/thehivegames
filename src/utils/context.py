import contextlib
import os
from contextvars import ContextVar
from starlette.exceptions import HTTPException
from starlette.responses import JSONResponse
from starlette.middleware.base import BaseHTTPMiddleware, RequestResponseEndpoint
from starlette.requests import Request
from starlette.responses import Response

from src.utils.exceptions import GameNotFoundError

db_context = ContextVar('db-context')
ENV = os.getenv('ENV')


class DBContextPool:
  def __init__(self, db_engine):
    self._engine = db_engine
    self._conn = None
    self._in_transaction = False

  async def query(self, q):
    if not self._conn:
      async with self._engine.begin() as c:
        return await c.execute(q)

    return await self._conn.execute(q)

  @contextlib.asynccontextmanager
  async def transact(self):
    if self._in_transaction:
      async with self._conn.begin_nested():
        yield self._conn
    else:
      if not self._conn:
        self._conn = await self._engine.connect()
      self._in_transaction = True
      try:
        async with self._conn.begin():
          yield
      finally:
        self._in_transaction = False
        await self._conn.close()
        self._conn = None

  @property
  def engine(self):
    return self._engine


class DBContext:
  request: Request
  db: DBContextPool

  def __init__(self, request, *, db_engine):
    if request:
      self.request = request
      # auth_header = request.headers.get('authorization')

    self.db = DBContextPool(db_engine)


def get_context() -> DBContext:
  return db_context.get()


class DBContextMiddleware(BaseHTTPMiddleware):
  async def dispatch(
      self, request: Request, call_next: RequestResponseEndpoint
  ) -> Response:
    if request.url.path.startswith('/_'):
      return await call_next(request)
    # noinspection PyBroadException
    try:
      ctx = DBContext(request, db_engine=request.app.state.db_engine)
      db_context.set(ctx)
      response = await call_next(request)
    except GameNotFoundError:
      return JSONResponse({'message': 'Game not found'}, status_code=400)
    except HTTPException as e:
      return JSONResponse({'message': e.detail}, status_code=e.status_code)
    except Exception as e:
      import traceback
      traceback.print_exc()
      return JSONResponse({'message': 'Internal Service Error'}, status_code=500)
    return response
