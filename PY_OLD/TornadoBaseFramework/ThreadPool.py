import threading


class ThreadPool:
    def __init__(self, list_of_args, thread_target, max_count=50):
        self.list_of_args = list_of_args
        self.thread_target = thread_target

        self._max_count = min(max_count, len(list_of_args))
        self._threads = None

    def _target(self):
        while len(self.list_of_args) > 0:
            args = self.list_of_args.pop()
            self.thread_target(*args)

    def start(self):
        self._threads = []
        for i in range(self._max_count):
            t = threading.Thread(target=self._target)
            self._threads.append(t)
            t.start()

    def join(self):
        for t in self._threads:
            t.join()
