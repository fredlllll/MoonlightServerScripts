import string
import urllib.parse
from random import *
import logging
import re

logger = logging.getLogger(__name__)


def generate_random_string(length=12, dictionary=string.ascii_uppercase + string.digits):
    return "".join(choice(dictionary) for _ in range(length))


def urlencode(query_arguments):
    return urllib.parse.urlencode(query_arguments, quote_via=urllib.parse.quote)


def format_milliseconds(input_time):
    input_time = int(input_time) / 1000
    if input_time >= 3600:
        return str(round(input_time / 3600, 2)) + ' Hours'
    elif input_time >= 60:
        return str(round(input_time / 60, 2)) + ' Minutes'
    else:
        return str(round(input_time, 2)) + ' Seconds'


def lreplace(pattern, sub, string):
    """
    Replaces 'pattern' in 'string' with 'sub' if 'pattern' starts 'string'.
    """
    return re.sub('^%s' % pattern, sub, string)


def rreplace(pattern, sub, string):
    """
    Replaces 'pattern' in 'string' with 'sub' if 'pattern' ends 'string'.
    """
    return re.sub('%s$' % pattern, sub, string)


def urljoin(*args):
    if len(args) > 0:
        start = args[0]
        for i in range(1, len(args)):
            start = urllib.parse.urljoin(start + '/', args[i])
        return start
    return ''


def as_float_or_default(value, default=0.0):
    try:
        return float(value)
    except ValueError:
        return default


def is_float(value):
    try:
        float(value)
        return True
    except ValueError:
        return False


def as_int_or_default(value, default=0):
    try:
        return int(value)
    except ValueError:
        return default


def is_int(value):
    try:
        int(value)
        return True
    except ValueError:
        return False


def clamp(value, from_, to):
    if value <= from_:
        return from_
    elif value >= to:
        return to
    return value
