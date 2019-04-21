import random
import asyncio
import aiohttp

from app.check import check, result, response_by_code, UP_CODES
from app.check import NoDomainError, ConnectionFailedError
from app.statuses import Up, Down, Unknown


def test_check():
    async def check_with_session(domain, timeout=1):
        session = aiohttp.ClientSession()
        answer = await check(domain, timeout, session)
        await session.close()
        return answer

    res = asyncio.run(check_with_session('google.com'))
    assert isinstance(res, dict)
    assert res['status'] == str(Up())
    assert res['code'] in UP_CODES

    res = asyncio.run(check_with_session('httpstat.us/500'))
    assert res['status'] == str(Down())
    assert res['code'] == 500


def test_result():
    async def result_with_session(domain, timeout=1):
        session = aiohttp.ClientSession()
        answer = await result(domain, timeout, session)
        await session.close()
        return answer

    res = asyncio.run(result_with_session('google.de'))
    assert isinstance(res, Up)

    res = asyncio.run(result_with_session(''))
    assert isinstance(res, Unknown) and res.extra == NoDomainError.__name__

    res = asyncio.run(result_with_session('test.tttddd2t'))
    assert isinstance(res, Unknown) and res.extra == ConnectionFailedError.__name__


def test_response_by_code():
    assert isinstance(response_by_code(200), Up)
    assert isinstance(response_by_code(500), Down)
    assert isinstance(response_by_code(random.choice(UP_CODES)), Up)
