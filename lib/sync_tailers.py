import threading
from typing import Optional
import subprocess

from typing.io import IO

from lib.websocket.websockets import Websockets


class ProcessTailer:
    def __init__(self, process: subprocess.Popen, websocket_channel: str):
        self.websocket_channel = websocket_channel
        self.process: subprocess.Popen = process

        self.running = False

        self._std_out_thread: Optional[threading.Thread] = None
        self._std_err_thread: Optional[threading.Thread] = None

    def start(self):
        self.running = True

        self._std_out_thread = threading.Thread(target=self._create_runner(self.process.stdout))
        self._std_err_thread = threading.Thread(target=self._create_runner(self.process.stderr))

        self._std_out_thread.start()
        self._std_err_thread.start()

    def _create_runner(self, stream: IO):
        def run():
            while self.running:
                data = stream.read()
                if not data:  # empty data indicates EOS
                    break
                text = data.decode()
                Websockets.enqueue_to_channel(self.websocket_channel, text)

        return run()

    def stop(self):
        self.running = False

    def join(self):
        self._std_out_thread.join()
        self._std_err_thread.join()


class FileTailer:
    def __init__(self, websocket_channel: str, path: str):
        self.path = path
        self.websocket_channel = websocket_channel
        self.process_tailer: ProcessTailer = None

    def start(self):
        self.process_tailer = ProcessTailer(subprocess.Popen(f'tail -F "{self.path}"', stdout=subprocess.PIPE, stderr=subprocess.PIPE), self.websocket_channel)
        self.process_tailer.start()

    def stop(self):
        self.process_tailer.stop()

    def join(self):
        self.process_tailer.join()
