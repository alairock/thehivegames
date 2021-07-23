from starlette.routing import Route, Mount
from pathlib import Path
from src.handlers import lobby, users, home
from src.secret_hitler import http_handler as sh
from starlette.staticfiles import StaticFiles

ROUTES = []

static = StaticFiles(directory=str(Path(__file__).parent.parent / "static"))


def routes():
    return [
        # static files
        Route('/', endpoint=home.homepage),
        Mount("/static", static, name="static"),

        # Lobby endpoints
        add_route('lobby.create', lobby.create_lobby_handler),
        add_route('lobby.join', lobby.join_lobby_handler),
        add_route('lobby.leave', lobby.leave_lobby_handler),
        add_route('lobby.events', lobby.events_handler, method='GET'),

        # Game endpoints
        add_route('game.start', lobby.start_game_handler),
        add_route('game.end', lobby.end_game_handler),

        # Users endpoints
        # add_route('users.list', users.list_users_handler),
        # add_route('users.create', users.create_user_handler),
        # add_route('users.update', users.update_user_handler),

        # Secret hitler endpoints
        add_route('sh.events', sh.event_handler, method='GET'),
        add_route('sh.get_users', sh.get_users),
        add_route('sh.nominate_chancellor', sh.select_chancellor)
    ]


def add_route(route, callback, method='POST'):
    route_prefix = route.lstrip('/').split('.')[0] + '.#'
    if route_prefix not in ROUTES:
        ROUTES.append(route_prefix)
    return Route('/api/' + route, callback, methods=[method])
