from aiohttp import ClientSession, ClientTimeout
from .statuses import Up, Down, Unknown

MAX_TIMEOUT = 5.0
UP_CODES = [200, 301, 302, 307, 308]


class CheckError(Exception):
    pass


class NoDomainError(CheckError):
    pass


class ConnectionFailedError(CheckError):
    pass


async def check(domain: str, timeout: int or float, session: ClientSession) -> dict:
    res = await result(domain, timeout, session)
    check_result = {'status': str(res)}

    if isinstance(res, Unknown):
        check_result['error'] = res.extra
    elif isinstance(res, (Up, Down)):
        check_result['code'] = res.code

    return check_result


async def result(domain: str, timeout: int or float, session: ClientSession) -> (Up, Down, Unknown):
    if not domain:
        return Unknown(extra=NoDomainError.__name__)

    try:
        async with session.get('http://' + domain, timeout=ClientTimeout(total=timeout), allow_redirects=False) as resp:
            return response_by_code(resp.status)
    except Exception as e:
        return Unknown(extra=ConnectionFailedError.__name__)


def response_by_code(code: int) -> Up or Down:
    return Up(code) if code in UP_CODES else Down(code)
