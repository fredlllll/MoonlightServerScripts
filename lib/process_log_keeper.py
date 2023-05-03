from lib.tailers import ProcessTailer
from lib.settings import Settings
import asyncio


class ProcessLogKeeper:
    def __init__(self, commandline, websocket_channel):
        self.commandline = commandline
        self.websocket_channel = websocket_channel
        self.log = ""

        self.process_tailer: ProcessTailer = None

    def get_text_handler(self):
        slf = self

        async def handler(text: str):
            slf.log += text
            slf.log = slf.log[-3000:]  # keep last 3000 characters

        return handler

    async def start(self):
        if Settings.debug_windows:
            self.process_tailer = ProcessTailer(None,self.websocket_channel)
        else:
            self.process_tailer = ProcessTailer(await asyncio.create_subprocess_exec(self.commandline, stdout=asyncio.subprocess.PIPE, stderr=asyncio.subprocess.PIPE), self.websocket_channel)
        self.process_tailer.text_handler = self.get_text_handler()
        self.process_tailer.start()
