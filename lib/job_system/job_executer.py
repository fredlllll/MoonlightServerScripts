import threading
import logging
from typing import Optional

logger = logging.getLogger(__name__)


class JobExecuter:
    jobs = []
    t: Optional[threading.Thread] = None

    @classmethod
    def add_job(cls, job):
        cls.jobs.append(job)
        if cls.t is None or not cls.t.is_alive():
            cls.t = threading.Thread(target=cls._run, daemon=True)
            cls.running = True
            cls.t.start()

    @classmethod
    def _run(cls):
        while True:
            if len(cls.jobs) > 0:
                j = cls.jobs.pop(0)
                try:
                    j.execute()
                except:  # so we don't crash accidentally
                    logger.exception("Exception when executing job")
            else:
                cls.t = None
                break
