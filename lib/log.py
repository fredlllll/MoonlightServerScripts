import logging
import logging.handlers
import os
import sys
from lib.log_timestamper import LogTimestamper
from lib.settings import Settings

timestamper = LogTimestamper(600)


def init_logging():
    log_file_path = os.path.realpath(Settings.log_file_location)

    if not os.path.exists(os.path.dirname(log_file_path)):
        raise Exception('log dir doesnt exist: ' + os.path.dirname(log_file_path))
    if os.path.exists(log_file_path) and not os.access(log_file_path, os.R_OK):
        raise Exception('dont have write access to ' + log_file_path)

    rotating_file_handler = logging.handlers.RotatingFileHandler(log_file_path, maxBytes=5000000, backupCount=10)
    stream_handler = logging.StreamHandler(sys.stdout)

    handlers = [rotating_file_handler, stream_handler]
    logging.basicConfig(level=logging.INFO, handlers=handlers)
    timestamper.start()
