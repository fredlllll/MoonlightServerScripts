from lib.settings import Settings
import os


def get_service_file_name(server_id):
    if Settings.debug_windows:
        return f"C:\\moondash_debug\\arma3server_{server_id}.service"
    return f"/etc/systemd/system/arma3server_{server_id}.service"


def get_startup_script_file_name(server_id):
    if Settings.debug_windows:
        return f"C:\\moondash_debug\\arma3server_{server_id}_startup.sh"
    user = Settings.arma_3_server_user
    return f"/home/{user}/arma3server_{server_id}_startup.sh"


def get_basic_config_file_name(server_id):
    if Settings.debug_windows:
        return f"C:\\moondash_debug\\{server_id}_basic.cfg"
    return os.path.join(Settings.arma_3_server_dir, server_id + "_basic.cfg")


def get_server_config_file_name(server_id):
    if Settings.debug_windows:
        return f"C:\\moondash_debug\\{server_id}_server.cfg"
    return os.path.join(Settings.arma_3_server_dir, server_id + "_server.cfg")


def get_server_profile_file_name(server_id):
    if Settings.debug_windows:
        return f"C:\\moondash_debug\\{server_id}.arma3profile"
    return os.path.join(Settings.arma_3_server_dir, server_id, server_id + ".arma3profile")
