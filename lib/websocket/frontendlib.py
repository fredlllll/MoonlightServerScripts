from sanic import Request, Websocket
from lib.websocket.websockets import Websockets
import json
import logging

logger = logging.getLogger(__name__)


async def frontendlib(request: Request, ws: Websocket):
    await Websockets.add_socket(ws)
    try:
        async for data in ws:
            msg = json.loads(data)
            message_type = msg['message_type']
            payload = msg['payload']
            if message_type == 'call':
                answer_id = payload['answer_id']
                function_name = payload['function_name']
                args = payload['args']
                request.app.add_task(Websockets.call_function(answer_id, ws, function_name, args))
            else:
                pass
    finally:
        await Websockets.remove_socket(ws)
