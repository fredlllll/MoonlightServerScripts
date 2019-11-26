from Util import escape_mod_name, get_mod_name, mount_dir
from ChooseOptions import Option, ChooseOptions
from STATICS import *
import subprocess


def mount_mod(mod_folder_path, target_path):
    os.makedirs(target_path, exist_ok=True)  # make the target dir
    mount_dir(mod_folder_path, target_path)
    print("linked " + os.path.basename(target_path))


def copy_mod(mod_folder_path, target_path):
    # shutil is too slow, lets use the real programs
    if os.path.exists(target_path):
        subprocess.check_call(['/bin/rm', '-rf', target_path])
    subprocess.check_call(['/bin/cp', '-r', mod_folder_path, target_path])


def link_mods(mod_ids):
    options = [
        Option("copy mods instead of mounting?", "copy", False)
    ]

    choose_options = ChooseOptions(options)
    kwargs = choose_options.choose_options()

    link_method = mount_mod
    if kwargs['copy']:
        link_method = copy_mod

    # we have to mount the mod folders instead of copying or linking
    for mod_id in mod_ids:
        mod_name = escape_mod_name(get_mod_name(mod_id))
        mod_path = os.path.join(STEAMFOLDER, 'SteamApps/workshop/content', str(ARMA3APPID), str(mod_id))
        target_path = os.path.join(ARMA3MODSDIR, '@' + mod_name)
        link_method(mod_path, target_path)
