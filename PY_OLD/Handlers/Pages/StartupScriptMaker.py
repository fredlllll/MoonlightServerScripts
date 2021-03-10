from Handlers.MoonlightBaseHandler import MoonlightBaseHandler
from tornado.web import authenticated
from TornadoBaseFramework.Settings import Settings
import logging
import os
from Util import md5

logger = logging.getLogger(__name__)


class StartupScriptMakerHandler(MoonlightBaseHandler):
    """
    renders the page_index.html template
    """
    url = '/startup_script_maker'

    def _get_mod_infos(self):
        mod_names = []
        if not os.path.exists(Settings.ARMA3MODSDIR):
            return []
        entries = os.listdir(Settings.ARMA3MODSDIR)
        for entry in entries:
            if os.path.isdir(os.path.join(Settings.ARMA3MODSDIR, entry)):
                mod_names.append(entry)

        mod_infos = []
        for mod_name in mod_names:
            mod_infos.append({
                'name': mod_name,
                'hash': md5(mod_name)
            })
        return mod_infos

    @authenticated
    def get(self, *args, **kwargs):
        mod_infos = self._get_mod_infos()

        self.render("page_startup_script_maker.html", mod_infos=mod_infos)

    @authenticated
    def post(self):
        mod_infos = self._get_mod_infos()
        checked_mods = []

        for info in mod_infos:
            if self.get_argument('chk_' + info['hash'], None) is not None:
                checked_mods.append(info)

        content = "#!/bin/bash\n"
        content += 'cd "' + Settings.ARMA3SERVERDIR + '"\n'
        content += './arma3server ' + Settings.ARMA3SERVERADDITONALCOMMANDLINE + ' -mod="\\\n'

        for mod in checked_mods:
            abs_path = os.path.join(Settings.ARMA3MODSDIR, mod['name'])
            rel_path = os.path.relpath(abs_path, Settings.ARMA3SERVERDIR)
            content += rel_path + ';\\\n'

        content += '"'

        with open(Settings.ARMA3SERVERRUNSCRIPT, 'w') as f:
            f.write(content)
        self.redirect(self.url)
