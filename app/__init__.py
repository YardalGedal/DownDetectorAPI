from typing import NoReturn

from aiohttp import web
from aiohttp import ClientSession
from .check import check, MAX_TIMEOUT
from .check import NoDomainError, ConnectionFailedError

__all__ = ['run']

PORT = 8888


async def handler(request: web.Request) -> web.Response:
    domain = request.rel_url.query.get('domain', '') or request.match_info.get('domain', '')

    try:
        timeout = float(min(request.rel_url.query.get('timeout', MAX_TIMEOUT), MAX_TIMEOUT))
    except ValueError:
        timeout = MAX_TIMEOUT

    return web.json_response(await check(domain, timeout, request.app['session']))


def run() -> NoReturn:
    app = web.Application()
    add_session(app)
    app.add_routes([web.get('/', handler), web.get('/domain/{domain}', handler)])
    web.run_app(app, port=PORT, reuse_port=True)


def add_session(app: web.Application) -> None:
    app['session'] = ClientSession()
    app.on_shutdown.append(lambda a: a['session'].close())
