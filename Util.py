import logging
import os
import hashlib
import shutil

logger = logging.getLogger(__name__)


def rename_in_place(file_path, new_file_name):
    dir_name = os.path.dirname(file_path)
    os.rename(file_path, os.path.join(dir_name, new_file_name))


# def mount_dir(original_path, link_path):
# only works as root
#    check_call(["sudo", "mount", "--bind", original_path, link_path])


def md5(s):
    return hashlib.md5(s.encode()).hexdigest()


def delete_folder_contents(folder):
    for entry in os.listdir(folder):
        path = os.path.join(folder, entry)
        if os.path.isdir(path):
            shutil.rmtree(path)
        elif os.path.isfile(path):
            os.unlink(path)
