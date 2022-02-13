import threading
import time
import signal


class JobExecuter:
    jobs = []
    t = None
    running = False

    @classmethod
    def init(cls):
        cls.t = threading.Thread(target=cls._run)

    @classmethod
    def start(cls):
        cls.running = True
        cls.t.start()

    @classmethod
    def stop(cls):
        cls.running = False

    @classmethod
    def add_job(cls, job):
        cls.jobs.append(job)

    @classmethod
    def _run(cls):
        while cls.running:
            if len(cls.jobs) > 0:
                j = cls.jobs.pop(0)
                try:
                    j.execute()
                except:  # so we dont crash accidentally
                    pass
            else:
                time.sleep(1)


JobExecuter.init()
JobExecuter.start()

signal.signal(signal.SIGINT, lambda signo, frame: JobExecuter.stop())
signal.signal(signal.SIGTERM, lambda signo, frame: JobExecuter.stop())
