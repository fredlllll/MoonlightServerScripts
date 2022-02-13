import random
from passlib.apps import custom_app_context
import string
import hashlib
import os
import shutil


def get_resource_id(resource_type):
    letters = string.ascii_lowercase + string.digits
    result_str = ''.join(random.choice(letters) for _ in range(32))
    return f'{resource_type}_{result_str}'


def get_random_string(length=32):
    letters = string.ascii_lowercase + string.digits
    result_str = ''.join(random.choice(letters) for i in range(length))
    return result_str


def hash_password(password):
    return custom_app_context.hash(password)


def verify_password(password, hash):
    return custom_app_context.verify(password, hash)


def md5(s: str):
    return hashlib.md5(s.encode()).hexdigest()


def rename_in_place(file_path, new_file_name):
    dir_name = os.path.dirname(file_path)
    os.rename(file_path, os.path.join(dir_name, new_file_name))


def delete_folder_contents(folder):
    for entry in os.listdir(folder):
        path = os.path.join(folder, entry)
        if os.path.isdir(path):
            shutil.rmtree(path)
        elif os.path.isfile(path):
            os.unlink(path)
