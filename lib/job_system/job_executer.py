import threading
import signal


class JobExecuter:
    jobs = []
    t: threading.Thread = None
    running = False

    @classmethod
    def stop(cls):
        cls.running = False

    @classmethod
    def add_job(cls, job):
        if cls.t is None or not cls.t.is_alive() or not cls.running:
            cls.t = threading.Thread(target=cls._run, daemon=True)
            cls.running = True
            cls.t.start()
        cls.jobs.append(job)

    @classmethod
    def _run(cls):
        while cls.running:
            if len(cls.jobs) > 0:
                j = cls.jobs.pop(0)
                try:
                    j.execute()
                except:  # so we don't crash accidentally
                    pass
            else:
                cls.running = False  # end thread if no jobs


signal.signal(signal.SIGINT, lambda signo, frame: JobExecuter.stop())
signal.signal(signal.SIGTERM, lambda signo, frame: JobExecuter.stop())
