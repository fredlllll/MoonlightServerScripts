from JobSystem.Job import Job
from APIs.SteamAPI import get_mod_name, escape_mod_name
from Settings.Settings import STEAMFOLDER, ARMA3APPID, ARMA3MODSDIR
from Util import delete_folder_contents
import os


class LinkModsJob(Job):
    def __init__(self, mod_ids):
        super().__init__('Link Mods', 'Mod Ids: ' + ', '.join(mod_ids))
        self.mod_ids = mod_ids

    def _run(self):
        workshop_mods_folder = os.path.join(STEAMFOLDER, 'SteamApps/workshop/content/', str(ARMA3APPID))

        delete_folder_contents(ARMA3MODSDIR)

        for mod_id in self.mod_ids:
            mod_folder = os.path.join(workshop_mods_folder, mod_id)
            mod_name = get_mod_name(mod_id)
            target_folder = os.path.join(ARMA3MODSDIR, '@' + escape_mod_name(mod_name))  # escape mod name
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
