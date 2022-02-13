import logging
import logging.handlers
import queue


def init_logging():
    log_queue = queue.Queue(-1)
    queue_handler = logging.handlers.QueueHandler(log_queue)
    log_handler = logging.StreamHandler()
    queue_listener = logging.handlers.QueueListener(log_queue, log_handler)
    queue_listener.start()
    logging.root.level = logging.INFO
    logging.root.addHandler(queue_handler)
