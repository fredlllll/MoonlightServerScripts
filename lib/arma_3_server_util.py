from lib.settings import Settings
from lib.apis.steam import get_arma_3_server_folder
import os


def get_service_file_name(server_id: str):
    if Settings.debug_windows:
        return f"C:\\moondash_debug\\arma3server_{server_id}.service"
    return f"/etc/systemd/system/arma3server_{server_id}.service"


def get_startup_script_file_name(server_id: str):
    if Settings.debug_windows:
        return f"C:\\moondash_debug\\arma3server_{server_id}_startup.sh"
    homedir = os.path.expanduser('~')
    return f"{homedir}/arma3server_{server_id}_startup.sh"


def get_basic_config_file_name(server_id: str):
    if Settings.debug_windows:
        return f"C:\\moondash_debug\\{server_id}_basic.cfg"
    return os.path.join(get_arma_3_server_folder(), server_id + "_basic.cfg")


def get_server_config_file_name(server_id: str):
    if Settings.debug_windows:
        return f"C:\\moondash_debug\\{server_id}_server.cfg"
    return os.path.join(get_arma_3_server_folder(), server_id + "_server.cfg")


def get_server_profile_file_name(server_id: str):
    if Settings.debug_windows:
        return f"C:\\moondash_debug\\{server_id}.arma3profile"
    return os.path.join(get_arma_3_server_folder(), server_id, server_id + ".arma3profile")


def get_server_mods_folder(server_id: str):
    return os.path.join(get_arma_3_server_folder(), 'mods', server_id)
