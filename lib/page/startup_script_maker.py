from lib.settings import Settings
from lib.util import md5
from lib.jinja_templates import get_template
from sanic.response import html, redirect
import logging
import os

logger = logging.getLogger(__name__)


def get_mod_infos():
    mod_names = []
    if not os.path.exists(Settings.arma_3_mods_dir):
        return []
    entries = os.listdir(Settings.arma_3_mods_dir)
    for entry in entries:
        if os.path.isdir(os.path.join(Settings.arma_3_mods_dir, entry)):
            mod_names.append(entry)

    mod_infos = []
    for mod_name in mod_names:
        mod_infos.append({
            'name': mod_name,
            'hash': md5(mod_name)
        })
    return mod_infos


async def startup_script_maker(request):
    mod_infos = get_mod_infos()

    template = await get_template("startup_script_maker.html", request)

    return html(template.render(mod_infos=mod_infos))


async def startup_script_maker_post(request):
    mod_infos = get_mod_infos()
    checked_mods = []

    for info in mod_infos:
        if request.form.get('chk_' + info['hash'], None) is not None:
            checked_mods.append(info)

    content = "#!/bin/bash\n"
    content += 'cd "' + Settings.arma_3_server_dir + '"\n'
    content += './arma3server ' + Settings.arma_3_server_additional_commandline + ' -mod="\\\n'

    for mod in checked_mods:
        abs_path = os.path.join(Settings.arma_3_mods_dir, mod['name'])
        rel_path = os.path.relpath(abs_path, Settings.arma_3_server_dir)
        content += rel_path + ';\\\n'

    content += '"'

    with open(Settings.arma_3_server_run_script, 'w') as f:
        f.write(content)
    return redirect('/startup_script_maker')
