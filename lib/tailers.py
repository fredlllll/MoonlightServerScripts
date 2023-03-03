import sanic
import asyncio
import asyncio.subprocess
from lib.websocket.websockets import Websockets


class ProcessTailer:
    def __init__(self, process: asyncio.subprocess.Process, websocket_channel: str):
        self.websocket_channel = websocket_channel
        self.process: asyncio.subprocess.Process = process

        self.running = False
        self.done = False

        self._done_counter = 0
        self.done_event = asyncio.Event()

    def start(self):
        self.running = True
        app = sanic.Sanic.get_app('sanic')
        app.add_task(self._create_runner(self.process.stdout))
        app.add_task(self._create_runner(self.process.stderr))

    def _create_runner(self, stream: asyncio.StreamReader):
        async def run():
            while self.running:
                data = await stream.read()
                if not data:  # empty data indicates EOS
                    break
                text = data.decode()
                await Websockets.broadcast_to_channel(self.websocket_channel, text)
            if self._done_counter > 0:
                self.done = True
                self.done_event.set()
                self.running = False
            else:
                self._done_counter += 1

        return run()


class FileTailer:
    def __init__(self, websocket_channel: str, path: str):
        self.path = path
        self.websocket_channel = websocket_channel
        self.process_tailer: ProcessTailer = None

    async def start(self):
        self.process_tailer = ProcessTailer(await asyncio.create_subprocess_exec(f'tail -F "{self.path}"', stdout=asyncio.subprocess.PIPE, stderr=asyncio.subprocess.PIPE), self.websocket_channel)
        self.process_tailer.start()
