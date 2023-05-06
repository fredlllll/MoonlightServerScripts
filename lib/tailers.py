import sanic
import asyncio
import asyncio.subprocess
import logging
from lib.websocket.websockets import Websockets
from lib.settings import Settings

logger = logging.getLogger(__name__)


class ProcessTailer:
    def __init__(self, process: asyncio.subprocess.Process, websocket_channel: str):
        self.websocket_channel = websocket_channel
        self.process: asyncio.subprocess.Process = process

        self.running = False
        self.done = False

        self._done_counter = 0
        self.done_event = asyncio.Event()

        self.text_handler = None

    def start(self):
        self.running = True
        app = sanic.Sanic.get_app('sanic')
        if Settings.debug_windows:
            app.add_task(self._create_debug_runner())
        else:
            logger.info("creating runners")
            app.add_task(self._create_runner(self.process.stdout))
            app.add_task(self._create_runner(self.process.stderr))

    def _create_debug_runner(self):
        async def run():
            while self.running:
                text = "i got some log\n"
                if self.text_handler is not None:
                    await self.text_handler(text)
                await Websockets.broadcast_to_channel(self.websocket_channel, text)
                await asyncio.sleep(1)

        return run()

    def _create_runner(self, stream: asyncio.StreamReader):
        async def run():
            async for line in stream:
                text = line.decode()
                if self.text_handler is not None:
                    await self.text_handler(text)
                await Websockets.broadcast_to_channel(self.websocket_channel, text)
            if self._done_counter > 0:
                self.done = True
                self.done_event.set()
                self.running = False
            else:
                self._done_counter += 1

        return run()

    def stop(self):
        self.running = False


class FileTailer:
    def __init__(self, websocket_channel: str, path: str):
        self.path = path
        self.websocket_channel = websocket_channel
        self.process_tailer: ProcessTailer = None

    async def start(self):
        self.process_tailer = ProcessTailer(await asyncio.create_subprocess_exec(f'tail -F "{self.path}"', stdout=asyncio.subprocess.PIPE, stderr=asyncio.subprocess.PIPE), self.websocket_channel)
        self.process_tailer.start()
