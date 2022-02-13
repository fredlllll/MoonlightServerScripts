import time
import os
from lib.util import get_random_string


def login_user(user):
    new_session_id = get_random_string(32)
    sess = Session(new_session_id, user.id)
    sessions[new_session_id] = sess
    return new_session_id


def logout(sess_id):
    del sessions[sess_id]
