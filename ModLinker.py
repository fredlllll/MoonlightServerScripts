from Util import escape_mod_name, get_mod_name, mount_dir
from STATICS import *


def link_mods(mod_ids):
    # we have to mount the mod folders instead of copying or linking
    for mod_id in mod_ids:
        mod_name = escape_mod_name(get_mod_name(mod_id))
        mod_path = os.path.join(STEAMFOLDER, 'SteamApps/workshop/content', str(ARMA3APPID), str(mod_id))
        link_path = os.path.join(ARMA3MODSDIR, '@' + mod_name)
        os.makedirs(link_path, exist_ok=True)  # make the target dir
        mount_dir(mod_path, link_path)
        print("linked " + mod_name)
