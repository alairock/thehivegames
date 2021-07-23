import asyncio
import json
from starlette.requests import Request
from starlette.responses import JSONResponse, StreamingResponse
from src.handlers.utils.lobby import create_lobby_code, leave_lobby, join_lobby, get_lobby_state, get_lobby_by_code
from src.handlers.utils.game import start_game
from src.handlers.utils.users import change_username, create_user
from src.utils.encodings import encode_dict


async def start_game_handler(request: Request):
  body = await request.json()
  await start_game(lobby_code=body.get('lobby_code'))
  return JSONResponse({'message': 'Start game'})


async def end_game_handler(request: Request):
  body = await request.json()
  await end_game(lobby_code=body.get('lobby_code'))
  return JSONResponse({'message': 'Ended game'})


async def create_lobby_handler(_):
  code = await create_lobby_code()
  return JSONResponse({'lobby_code': code})


async def leave_lobby_handler(request: Request):
  body = await request.json()
  await leave_lobby(user_id=body.get('user_id'), lobby_code=body.get('lobby_code'))
  return JSONResponse({})


async def username_change_handler(request: Request):
  body = await request.json()
  await change_username(user_id=body.get('user_id'), username=body.get('username'))
  return JSONResponse({})


async def join_lobby_handler(request: Request):
  body = await request.json()
  user = await create_user(body.get('username'))
  r = await join_lobby(body.get('lobby_code'), user.id)
  return JSONResponse({'user_id': r.user_id})


async def _event_stream(lobby_code):
  _error_response = ""
  _error_code = ""
  while True:
    event = await get_lobby_state(lobby_code)

    if event is None:
      _error_response = "No game state found"
      _error_code = "game_not_found"
      yield encode_dict(json.dumps({"error": _error_response, "code": _error_code}))
      await asyncio.sleep(3)
      continue
    elif len(event.get('members')) == 0:
      _error_response = "No members found"
      _error_code = "empty_lobby"
      yield encode_dict({"error": _error_response, "code": _error_code})
      await asyncio.sleep(3)
      continue
    yield encode_dict(event)
    await asyncio.sleep(1)


async def events_handler(request: Request):
  lobby_code = request.query_params.get('lobby_code')
  if not lobby_code:
    return JSONResponse({'error': 'game code not passed'}, 400)
  game = await get_lobby_by_code(lobby_code)
  if not game:
    return JSONResponse({'error': 'game not found'}, 400)

  headers = {
    "Content-Type": "text/event-stream",
    "Cache-Control": "no-cache",
    "Connection": "keep-alive",
    "X-Accel-Buffering": "no",
  }
  return StreamingResponse(_event_stream(lobby_code), headers=headers)

