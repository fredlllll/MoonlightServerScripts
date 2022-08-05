from lib.apis.steam import get_downloaded_mods, get_mod_name, escape_mod_name
from lib.settings import Settings
from lib.util import delete_folder_contents
from lib.jinja_templates import get_template
from lib.constants import ARMA3APPID
from sanic.response import html, redirect
import os
import logging

logger = logging.getLogger(__name__)


def get_mod_infos():
    mod_ids = get_downloaded_mods()

    mod_infos = []
    for mod_id in mod_ids:
        mod_infos.append({
            'id': mod_id,
            'name': get_mod_name(mod_id)
        })
    return mod_infos


def link_mods(mod_ids):
    workshop_mods_folder = os.path.join(Settings.steam_folder, 'steamapps/workshop/content/', str(ARMA3APPID))

    delete_folder_contents(Settings.arma_3_mods_dir)

    for mod_id in mod_ids:
        mod_folder = os.path.join(workshop_mods_folder, mod_id)
        mod_name = get_mod_name(mod_id)
        target_folder = os.path.join(Settings.arma_3_mods_dir, '@' + escape_mod_name(mod_name))  # escape mod name
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


async def mod_linker(request):
    mod_infos = get_mod_infos()
    template = get_template('mod_linker.html', request)
    return html(template.render(mod_infos=mod_infos))


async def mod_linker_post(request):
    mod_infos = get_mod_infos()
    checked_mod_ids = []

    for info in mod_infos:
        if request.form.get('chk_' + info['id'], None) is not None:
            checked_mod_ids.append(info['id'])

    link_mods(checked_mod_ids)
    return redirect('/mod_linker')
