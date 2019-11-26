#!/usr/bin/python3.8

# this script is supposed to fix issues with capitalization in filenames of mods
# this is done by linking instead of renaming so future updates dont break anything

import sys
import os
from Util import rename_in_place


def get_dir_files(dir_path, sub_dirs=True, follow_sym_links=False, full_paths=True, sym_links=False):
    dirs_to_search = [dir_path]
    all_files = []
    while len(dirs_to_search) > 0:
        current_dir = dirs_to_search.pop()
        dir_entries = os.listdir(current_dir)
        for entry in dir_entries:
            full_path = os.path.join(current_dir, entry)
            is_dir = os.path.isdir(full_path)
            is_link = os.path.islink(full_path)

            if is_dir:
                if not sub_dirs:
                    continue
                if not follow_sym_links and is_link:
                    continue
                dirs_to_search.append(full_path)
            else:
                if not sym_links and is_link:
                    continue
                if full_paths:
                    all_files.append(full_path)
                else:
                    all_files.append(entry)
    return all_files


def get_dir_dirs(dir_path, sym_links=False, full_paths=False):
    entries = os.listdir(dir_path)
    dirs = []
    for entry in entries:
        full_path = os.path.join(dir_path, entry)
        if not sym_links and os.path.islink(full_path):
            continue
        if os.path.isdir(full_path):
            if full_paths:
                dirs.append(full_path)
            else:
                dirs.append(entry)
    return dirs


def process_mod_sub_folder(sub_folder):
    if os.path.exists(sub_folder):
        sub_folder_files = get_dir_files(sub_folder)
        for file in sub_folder_files:
            name = os.path.basename(file)
            name_lower = name.lower()
            if name != name_lower:
                rename_in_place(file, name_lower)


def process_mod_folder(mod_folder):
    addons_folder = os.path.join(mod_folder, 'addons')
    keys_folder = os.path.join(mod_folder, 'keys')

    mod_dirs = get_dir_dirs(mod_folder)
    # check all folders of the mod to see if addons and keys are capitalized properly, if not make a lowercase link
    for mod_dir in mod_dirs:
        mod_dir_path = os.path.join(mod_folder, mod_dir)
        if mod_dir.lower() == 'addons' and mod_dir.lower() != mod_dir:
            rename_in_place(mod_dir_path, 'addons')
        elif mod_dir.lower() == 'keys' and mod_dir.lower() != mod_dir:
            rename_in_place(mod_dir_path, 'keys')

    # some mods may not have a keys or addons folder, hence we have to check if they(their links) exist
    if os.path.exists(addons_folder):
        process_mod_sub_folder(addons_folder)

    if os.path.exists(keys_folder):
        process_mod_sub_folder(keys_folder)


folder = sys.argv[1]  # the folder containing the mods
folders = get_dir_dirs(folder, sym_links=True)

for d in folders:
    if d.startswith('@'):  # mod folders start with @
        full_mod_path = os.path.join(folder, d)
        process_mod_folder(full_mod_path)
