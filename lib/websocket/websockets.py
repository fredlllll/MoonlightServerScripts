from sanic import Websocket
from threading import Lock
import json
import traceback
import logging
import sanic
import asyncio

logger = logging.getLogger(__name__)


class Websockets:
    sockets: list[Websocket] = []
    sockets_lock = Lock()
    callable_functions = dict[str, callable]
    enqueued_messages_lock = Lock()
    enqueued_messages = []

    @classmethod
    async def add_socket(cls, ws: Websocket):
        cls.sockets_lock.acquire()
        cls.sockets.append(ws)
        cls.sockets_lock.release()

    @classmethod
    async def remove_socket(cls, ws: Websocket):
        cls.sockets_lock.acquire()
        try:
            cls.sockets.remove(ws)
        except ValueError:
            pass  # doesnt matter if it exists or not
        cls.sockets_lock.release()

    @classmethod
    def enqueue_to_channel(cls, channel: str, data):
        cls.enqueued_messages_lock.acquire()
        cls.enqueued_messages.append((channel, data))
        cls.enqueued_messages_lock.release()

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
            pass

    @classmethod
    async def queue_loop(cls):
        while True:
            cls.enqueued_messages_lock.acquire()
            for item in cls.enqueued_messages:
                await cls.broadcast_to_channel(*item)
            cls.enqueued_messages.clear()
            cls.enqueued_messages_lock.release()
            await asyncio.sleep(0.1)

    @classmethod
    async def pinger(cls):
        while True:
            await Websockets.broadcast_to_channel("ping", "ping")
            await asyncio.sleep(2)
