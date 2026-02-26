import sys

from redis.asyncio import Redis
import asyncio
import uvicorn
from starlette.applications import Starlette
from starlette.requests import Request
from starlette.responses import FileResponse, Response
from starlette.routing import Route

from sse_starlette import EventSourceResponse # самая главная библиотека !!!


async def subscribe_stream(channel):
    redis = Redis(host='localhost', port=6379, db=0, decode_responses=True)
    sub = redis.pubsub()
    await sub.subscribe(channel)

    try:
        while True:
            msg = await sub.get_message(ignore_subscribe_messages=True, timeout=None)
            if msg:
                msg = str(msg)
                yield {"data": msg}
            await asyncio.sleep(0.1)
    except asyncio.CancelledError:
        # Выход по:
        # 1. Клиент закрыл панель
        # 2. Клиент вызвал eventSource.close()
        # 3. Сервер выключается
        # raise
        print("Отключение от браузера", flush=True)
    finally:
        try:
            await sub.unsubscribe(channel)
        except Exception as e:
            ...


async def subscribe_endpoint(request: Request) -> Response:
    """SSE endpoint."""
    channel = request.path_params.get("channel")
    if not channel:
        return Response(status_code=404)
    return EventSourceResponse(subscribe_stream(channel))


async def home_page(request: Request) -> FileResponse:
    return FileResponse(path="redis_demo.html")


app = Starlette(
    routes=[
        Route("/", endpoint=home_page),
        Route("/sub/{channel}", endpoint=subscribe_endpoint),
    ]
)

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
