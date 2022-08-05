import logging
from sanic.response import html
from lib.jinja_templates import get_template
from lib.db.models.arma_3_modset import Arma3Modset
from lib.db.models.arma_3_modset_mod import Arma3ModsetMod
from lib.apis.steam import get_mod_name

logger = logging.getLogger(__name__)


async def modsets(request):
    modsets_ = Arma3Modset.all()
    for modset in modsets_:
        mods = Arma3ModsetMod.where({'modset_id': modset.id})
        modset.mods = ', '.join([get_mod_name(m.mod_steam_id) for m in mods])

    template = get_template("modsets.html", request)
    return html(template.render(modsets=modsets_))


async def modsets_post(request):
    pass
