import logging
import os
from logging.handlers import RotatingFileHandler
from Framework.LogTimestamper import LogTimestamper
from Settings.Settings import LOG_FILE_LOCATION

timestamper = LogTimestamper()


def init_logging():
    if not os.path.exists(os.path.dirname(LOG_FILE_LOCATION)):
        raise Exception('log dir doesnt exist: ' + os.path.dirname(LOG_FILE_LOCATION))
    if os.path.exists(LOG_FILE_LOCATION) and not os.access(LOG_FILE_LOCATION, os.R_OK):
        raise Exception('dont have write access to ' + LOG_FILE_LOCATION)

    rotating_file_handler = RotatingFileHandler(LOG_FILE_LOCATION, maxBytes=5000000, backupCount=10)
    stream_handler = logging.StreamHandler()  # logs to stderr

    handlers = [rotating_file_handler, stream_handler]
    logging.basicConfig(level=logging.INFO, handlers=handlers)
    timestamper.start()
