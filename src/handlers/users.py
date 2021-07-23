from starlette.requests import Request
from starlette.responses import JSONResponse

from src.handlers.utils.lobby import get_lobby_by_code
from src.handlers.utils.users import list_users, create_user, change_username


async def list_users_handler(request: Request):
    body = await request.json()
    lobby_code = body.get('lobby_code')
    lobby = await get_lobby_by_code(lobby_code)
    users = await list_users(lobby.id)

    return JSONResponse({'users': {user['user_id']: user['username'] for user in users}})


async def create_user_handler(request: Request):
    body = await request.json()
    username = body.get('username')
    user = await create_user(username)
    return JSONResponse({'user': user})


async def update_user_handler(request: Request):
    body = await request.json()
    username = body.get('username')
    user_id = body.get('user_id')
    user = await change_username(user_id, username)
    return JSONResponse({'user': user})
