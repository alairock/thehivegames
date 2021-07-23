import asyncio
from starlette.requests import Request
from starlette.responses import JSONResponse, StreamingResponse
from src.secret_hitler.elections import nominate_chancellor, get_election_cycle
from src.secret_hitler.state import get_sh_state, get_players_info
from src.handlers.utils.lobby import get_lobby_by_code
from src.utils.encodings import encode_dict


async def get_users(request: Request):
    body = await request.json()
    lobby_code = body.get('lobby_code')
    user_id = body.get('user_id')
    if not lobby_code:
        return JSONResponse({'error': 'game not found'}, 400)
    game = await get_lobby_by_code(lobby_code)
    roles = await get_players_info(game.id, user_id)
    return JSONResponse({'roles': roles})


async def select_chancellor(request: Request):
    body = await request.json()
    lobby_code = body.get('lobby_code')
    nominee = body.get('nominee')
    if not all([lobby_code, nominee]):
        return JSONResponse({'error': 'game not found'}, 400)
    game = await get_lobby_by_code(lobby_code)
    election = await get_election_cycle(game.id)
    await nominate_chancellor(game.id, election.id, nominee)
    return JSONResponse({'roles': 'roles'})


async def _event_stream(lobby_code):
    while True:
        lobby = await get_lobby_by_code(lobby_code)
        game_state = await get_sh_state(lobby.id)
        yield encode_dict(game_state)
        await asyncio.sleep(3)


async def event_handler(request: Request):
    headers = {
        "Content-Type": "text/event-stream",
        "Cache-Control": "no-cache",
        "Connection": "keep-alive",
        "X-Accel-Buffering": "no",
    }

    lobby_code = request.query_params.get('lobby_code')
    if not lobby_code:
        return JSONResponse({'error': 'game code not passed'}, 400)
    game = await get_lobby_by_code(lobby_code)
    if not game:
        return JSONResponse({'error': 'game not found'}, 400)
    return StreamingResponse(_event_stream(lobby_code), headers=headers)
