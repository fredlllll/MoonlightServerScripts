#!/usr/bin/python3.8

from ModIdsCollector import get_mod_ids
from ChooseOptions import ChooseOptions, Option
from ModDownloader import download_mods
from ModLinker import link_mods
from RunScriptCreator import create_run_script


def process_mod_ids_list(mod_ids, do_download, do_linking, do_create_run_script):
    if do_download:
        download_mods(mod_ids)

    if do_linking:
        link_mods(mod_ids)

    if do_create_run_script:
        create_run_script(mod_ids)


def main():
    # get mod ids
    mod_ids = get_mod_ids()
    if mod_ids is None:
        print("no mod ids were chosen")
        return

    options = [
        Option("Do Download", "do_download", False),
        Option("Do Linking", "do_linking", True),
        Option("Do Create Run Script", "do_create_run_script", True)
    ]

    choose_options = ChooseOptions(options)
    kwargs = choose_options.choose_options()

    process_mod_ids_list(mod_ids, **kwargs)


main()
