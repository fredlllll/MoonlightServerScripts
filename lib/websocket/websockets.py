from sanic import Websocket
from threading import Lock
import json
import traceback
import logging
import sanic

logger = logging.getLogger(__name__)


class Websockets:
    sockets: list[Websocket] = []
    sockets_lock = Lock()
    callable_functions = dict[str, callable]

    @classmethod
    async def add_socket(cls, ws: Websocket):
        cls.sockets_lock.acquire()
        cls.sockets.append(ws)
        cls.sockets_lock.release()

    @classmethod
    async def remove_socket(cls, ws: Websocket):
        cls.sockets_lock.acquire()
        cls.sockets.remove(ws)
        cls.sockets_lock.release()

    @classmethod
    def enqueue_to_channel(cls, channel: str, data):
        async def run():
            await Websockets.broadcast_to_channel(channel, data)

        app = sanic.Sanic.get_app('sanic')
        app.add_task(run())

    @classmethod
    async def broadcast_to_channel(cls, channel: str, data):
        cls.sockets_lock.acquire()
        try:
            message = json.dumps(
                {
                    "message_type": "channel",
                    "payload": {
                        "channel": channel,
                        "data": data
                    }
                }
            )
            to_del = []
            for sock in cls.sockets:
                try:
                    await sock.send(message)
                except:  # TODO: check for right exception?
                    to_del.append(sock)
            for sock in to_del:
                cls.sockets.remove(sock)
        except:
            logger.exception("broadcast failed")
        finally:
            cls.sockets_lock.release()

    @classmethod
    async def call_function(cls, answer_id, ws, function_name, arguments):
        function = cls.callable_functions.get(function_name, None)
        try:
            result = await function(**arguments)
            payload = {
                "answer_id": answer_id,
                "result": result
            }
            await ws.send(json.dumps({
                "message_type": 'answer',
                "payload": payload
            }))
        except Exception as ex:
            payload = {
                "answer_id": answer_id,
                "exception": traceback.format_exception(ex)
            }
            await ws.send(json.dumps({
                "message_type": 'exception',
                "payload": payload
            }))
            pass  # TODO: send exception
