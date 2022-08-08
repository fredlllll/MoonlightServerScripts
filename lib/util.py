import random
from passlib.apps import custom_app_context
import string
import hashlib
import os
import shutil


def get_resource_id(resource_type: str) -> str:
    letters = string.ascii_lowercase + string.digits
    result_str = ''.join(random.choice(letters) for _ in range(32))
    return f'{resource_type}_{result_str}'


def get_random_string(length: int = 32) -> str:
    letters = string.ascii_lowercase + string.digits
    result_str = ''.join(random.choice(letters) for i in range(length))
    return result_str


def hash_password(password: str) -> str:
    return custom_app_context.hash(password)


def verify_password(password: str, hash: str) -> bool:
    return custom_app_context.verify(password, hash)


def md5(s: str) -> str:
    return hashlib.md5(s.encode()).hexdigest()


def rename_in_place(file_path: str, new_file_name: str):
    dir_name = os.path.dirname(file_path)
    os.rename(file_path, os.path.join(dir_name, new_file_name))


def delete_folder_contents(folder: str):
    if not os.path.exists(folder):
        return
    for entry in os.listdir(folder):
        path = os.path.join(folder, entry)
        if os.path.isdir(path):
            shutil.rmtree(path)
        elif os.path.isfile(path):
            os.unlink(path)


def copy(source_file: str, dst_file: str):
    os.makedirs(os.path.dirname(dst_file), exist_ok=True)
    shutil.copy(source_file, dst_file)


def indent(value: str, indent_str: str = '  ') -> str:
    return indent_str + value.replace('\n', '\n' + indent_str).rstrip(indent_str)
