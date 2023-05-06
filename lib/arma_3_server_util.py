from lib.settings import Settings
from lib.apis.steam import get_arma_3_server_folder
from lib.util import copy
from lib.process_log_keeper import ProcessLogKeeper
import os
import logging

logger = logging.getLogger(__name__)

server_log_keepers = {}


async def get_server_log_keeper(server_id: str) -> ProcessLogKeeper:
    log_keeper = server_log_keepers.get(server_id, None)
    if log_keeper is None:
        log_keeper = ProcessLogKeeper(['sudo', 'journalctl', '-u', server_id, '-n', '500','-f'], server_id)
        server_log_keepers[server_id] = log_keeper
        await log_keeper.start()
    return log_keeper


def get_service_file_name(server_id: str) -> str:
    if Settings.debug_windows:
        return f"C:\\moondash_debug\\arma3server_{server_id}.service"
    return f"/etc/systemd/system/arma3server_{server_id}.service"


def get_startup_script_file_name(server_id: str) -> str:
    if Settings.debug_windows:
        return f"C:\\moondash_debug\\arma3server_{server_id}_startup.sh"
    homedir = os.path.expanduser(f'~{Settings.local_steam_user}')
    return f"{homedir}/arma3server_{server_id}_startup.sh"


def get_basic_config_file_name(server_id: str) -> str:
    if Settings.debug_windows:
        return f"C:\\moondash_debug\\{server_id}_basic.cfg"
    return os.path.join(get_arma_3_server_folder(), server_id + "_basic.cfg")


def get_basic_config_content(server_id: str) -> str:
    path = get_basic_config_file_name(server_id)
    if not os.path.exists(path):
        copy("arma_server_default_files/basic.cfg", path, Settings.local_steam_user, Settings.local_steam_user)

    with open(path, 'rb') as f:
        return f.read().decode()


def set_basic_config_content(server_id: str, content: str):
    with open(get_basic_config_file_name(server_id), 'wb') as f:
        f.write(content.encode())


def get_server_config_file_name(server_id: str) -> str:
    if Settings.debug_windows:
        return f"C:\\moondash_debug\\{server_id}_server.cfg"
    return os.path.join(get_arma_3_server_folder(), server_id + "_server.cfg")


def get_server_config_content(server_id: str) -> str:
    path = get_server_config_file_name(server_id)
    if not os.path.exists(path):
        copy("arma_server_default_files/server.cfg", path, Settings.local_steam_user, Settings.local_steam_user)

    with open(path, 'rb') as f:
        return f.read().decode()


def set_server_config_content(server_id: str, content: str):
    with open(get_server_config_file_name(server_id), 'wb') as f:
        f.write(content.encode())


def get_server_profile_file_name(server_id: str) -> str:
    if Settings.debug_windows:
        return f"C:\\moondash_debug\\{server_id}.arma3profile"
    return os.path.join(get_arma_3_server_folder(), server_id, server_id + ".arma3profile")


def get_server_profile_content(server_id: str) -> str:
    path = get_server_profile_file_name(server_id)
    if not os.path.exists(path):
        copy("arma_server_default_files/server.arma3profile", path, Settings.local_steam_user, Settings.local_steam_user)

    with open(path, 'rb') as f:
        return f.read().decode()


def set_server_profile_content(server_id: str, content: str):
    with open(get_server_profile_file_name(server_id), 'wb') as f:
        f.write(content.encode())


def get_server_mods_folder(server_id: str) -> str:
    return os.path.join(get_arma_3_server_folder(), 'mods', server_id)
