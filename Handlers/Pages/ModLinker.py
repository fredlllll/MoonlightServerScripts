from Handlers.MoonlightBaseHandler import MoonlightBaseHandler
from tornado.web import authenticated
from APIs.SteamAPI import get_downloaded_mods, get_mod_name, escape_mod_name
from .Jobs import JobsHandler
from TornadoBaseFramework.Settings import Settings
from Util import delete_folder_contents
import os
import logging

logger = logging.getLogger(__name__)


class ModLinkerHandler(MoonlightBaseHandler):
    """
    renders the page_index.html template
    """
    url = '/mod_linker'

    def _get_mod_infos(self):
        mod_ids = get_downloaded_mods()

        mod_infos = []
        for mod_id in mod_ids:
            mod_infos.append({
                'id': mod_id,
                'name': get_mod_name(mod_id)
            })
        return mod_infos

    def _link_mods(self, mod_ids):
        workshop_mods_folder = os.path.join(Settings.STEAMFOLDER, 'SteamApps/workshop/content/', str(Settings.ARMA3APPID))

        delete_folder_contents(Settings.ARMA3MODSDIR)

        for mod_id in mod_ids:
            mod_folder = os.path.join(workshop_mods_folder, mod_id)
            mod_name = get_mod_name(mod_id)
            target_folder = os.path.join(Settings.ARMA3MODSDIR, '@' + escape_mod_name(mod_name))  # escape mod name
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

    @authenticated
    def get(self, *args, **kwargs):
        mod_infos = self._get_mod_infos()

        self.render("page_mod_linker.html", mod_infos=mod_infos)

    @authenticated
    def post(self):
        mod_infos = self._get_mod_infos()
        checked_mod_ids = []

        for info in mod_infos:
            if self.get_argument('chk_' + info['id'], None) is not None:
                checked_mod_ids.append(info['id'])

        self._link_mods(checked_mod_ids)

        self.redirect(JobsHandler.url)
