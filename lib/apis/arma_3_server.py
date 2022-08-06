from lib.settings import Settings
from lib.systemd_unit_controller import SystemdUnitController
from lib.mock_service_controller import MockServiceController
from lib.db.models.arma_3_modset import Arma3Modset
from lib.db.models.arma_3_modset_mod import Arma3ModsetMod
from lib.apis.steam import get_mod_name, escape_mod_name
from lib.arma_3_server_util import get_service_file_name, get_startup_script_file_name, get_server_mods_folder, get_basic_config_file_name, get_server_config_file_name
from lib.constants import ARMA3APPID
from lib.util import delete_folder_contents
import os
import subprocess
import logging

logger = logging.getLogger(__name__)

controllers = {}


def get_server_controller(server_id):
    cont = controllers.get(server_id, None)
    if cont is None:
        if Settings.debug_windows:
            cont = MockServiceController()
        else:
            cont = SystemdUnitController("arma3server_" + server_id + ".service")
        controllers[server_id] = cont
    return cont


def create_startup_script(server):
    file_name = get_startup_script_file_name(server.id)
    basic_config = os.path.basename(get_basic_config_file_name(server.id))
    server_config = os.path.basename(get_server_config_file_name(server.id))

    content = "#!/bin/bash\n"
    content += 'cd "' + Settings.arma_3_server_dir + '"\n'
    content += f'./arma3server -cfg={basic_config} -config={server_config} -name={server.id}'
    if server.additional_commandline:
        content += " " + server.additional_commandline
    content += ' -mod="\\\n'

    if server.modset_id:
        modset = Arma3Modset.find(server.modset_id)
        mods = Arma3ModsetMod.where({'modset_id': modset.id})

        for mod in mods:
            mod_name = get_mod_name(mod.mod_steam_id)
            abs_path = os.path.join(Settings.arma_3_mods_dir, server.id, '@' + mod_name)
            rel_path = os.path.relpath(abs_path, Settings.arma_3_server_dir)
            content += rel_path + ';\\\n'

    content += '"'

    with open(file_name, 'w') as f:
        f.write(content)


def create_service(server):
    """creates a service file for the server, and calls daemon-reload"""
    file_name = get_service_file_name(server.id)
    user = Settings.arma_3_server_user

    content = "[Unit]\nDescription=Arma 3 Server\n\n[Service]\nUser="
    content += user
    content += "\nGroup=" + user
    content += "\nWorkingDirectory=/home/" + user
    content += "\nExecStart=/bin/bash " + get_startup_script_file_name(server.id)
    content += "\nRestart=always\n\n[Install]\nWantedBy=multi-user.target\n"

    with open(file_name, 'w') as f:
        f.write(content)

    if Settings.debug_windows:
        logger.info("windows create service dummy")
        return

    subprocess.check_call("sudo systemctl daemon-reload")


def link_mods(server):
    if Settings.debug_windows:
        return

    if server.modset_id:
        modset = Arma3Modset.find(server.modset_id)
        mod_ids = [m.mod_steam_id for m in Arma3ModsetMod.where({'modset_id': modset.id})]
    else:
        mod_ids = []

    workshop_mods_folder = os.path.join(Settings.steam_folder, 'steamapps/workshop/content/', str(ARMA3APPID))
    server_mods_folder = get_server_mods_folder(server.id)

    delete_folder_contents(server_mods_folder)

    for mod_id in mod_ids:
        mod_folder = os.path.join(workshop_mods_folder, mod_id)
        mod_name = get_mod_name(mod_id)
        target_folder = os.path.join(server_mods_folder, '@' + escape_mod_name(mod_name))  # escape mod name
        os.makedirs(target_folder, exist_ok=True)  # create the @modname folder
        for abs_dir_path, sub_dirs, files in os.walk(mod_folder):
            rel_dir_path = os.path.relpath(abs_dir_path, mod_folder).lower()  # make folder names inside mod lowercase
            abs_target_dir_path = os.path.join(target_folder, rel_dir_path)
            for sub_dir in sub_dirs:  # create lowercase sub dirs
                abs_target_sub_dir_path = os.path.join(abs_target_dir_path, sub_dir.lower())
                os.makedirs(abs_target_sub_dir_path, exist_ok=True)
            for file in files:  # make lowercase links for files
                abs_file_path = os.path.join(abs_dir_path, file)
                abs_target_file_path = os.path.join(abs_target_dir_path, file.lower())
                os.symlink(abs_file_path, abs_target_file_path)


def start_server(server):
    cont = get_server_controller(server.id)
    link_mods(server)
    create_startup_script(server)
    cont.start()


def stop_server(server):
    cont = get_server_controller(server.id)
    cont.stop()


def restart_server(server):
    cont = get_server_controller(server.id)
    cont.stop()
    link_mods(server)
    create_startup_script(server)
    cont.start()


def disable_server(server):
    cont = get_server_controller(server.id)
    cont.disable()


def enable_server(server):
    cont = get_server_controller(server.id)
    cont.enable()
