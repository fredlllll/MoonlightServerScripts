import time
import traceback
import asyncio
from lib.db.models.job_info import JobInfo, WAITING, EXECUTING, FAILED, FINISHED


class Job:
    def __init__(self, name=None, info=None):
        self._job_info = JobInfo()
        self._job_info.name = name
        self._job_info.info = info
        self._job_info.status = WAITING
        self._job_info.error = 'None'
        self._job_info.output = ''
        self._job_info.progress = 0

        self._save_info()

    def _save_info(self):
        task = asyncio.run_coroutine_threadsafe(self._job_info.save(), asyncio.get_event_loop())
        while not task.done():
            time.sleep(0.1)

    def execute(self):
        self._job_info.start_timestamp = time.time()
        self._job_info.status = EXECUTING
        self._save_info()
        try:
            self._run()
            self._job_info.status = FINISHED
        except Exception as e:
            self._job_info.status = FAILED
            self._job_info.error = traceback.format_exc()
        self._job_info.end_timestamp = time.time()
        self._job_info.progress = 1
        self._save_info()

    def _update_progress(self, progress=0):
        self._job_info.progress = progress
        self._save_info()

    def _run(self):
        pass
