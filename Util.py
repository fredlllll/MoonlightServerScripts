import string
import urllib.parse
from random import *
import logging
import re
import os
import hashlib
import shutil
from subprocess import check_call

logger = logging.getLogger(__name__)


def generate_random_string(length=12, dictionary=string.ascii_uppercase + string.digits):
    return "".join(choice(dictionary) for _ in range(length))


def urlencode(query_arguments):
    return urllib.parse.urlencode(query_arguments, quote_via=urllib.parse.quote)


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


def is_float(value):
    try:
        float(value)
        return True
    except ValueError:
        return False


def is_int(value):
    try:
        int(value)
        return True
    except ValueError:
        return False


def try_parse_int(s, base=10, val=None):
    try:
        return int(s, base)
    except ValueError:
        return val


def clamp(value, from_, to):
    if value <= from_:
        return from_
    elif value >= to:
        return to
    return value


def rename_in_place(file_path, new_file_name):
    dir_name = os.path.dirname(file_path)
    os.rename(file_path, os.path.join(dir_name, new_file_name))


def mount_dir(original_path, link_path):
    # only works as root
    check_call(["sudo", "mount", "--bind", original_path, link_path])


def md5(s):
    return hashlib.md5(s.encode()).hexdigest()


def delete_folder_contents(folder):
    for entry in os.listdir(folder):
        path = os.path.join(folder, entry)
        if os.path.isdir(path):
            shutil.rmtree(path)
        elif os.path.isfile(path):
            os.unlink(path)
