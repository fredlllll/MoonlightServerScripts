import logging
from sanic.response import html, redirect
from lib.apis.steam import get_downloaded_mods, get_mod_name
from lib.jinja_templates import get_template
from lib.db.models.arma_3_modset_mod import Arma3ModsetMod
from lib.db.models.arma_3_modset import Arma3Modset
from lib.db.models.arma_3_server import Arma3Server
from lib.responses import response_404

logger = logging.getLogger(__name__)


async def modset(request, modset_id):
    modset_ = Arma3Modset.find(modset_id)
    if modset_ is None:
        return response_404(request)
    template = get_template("modset.html", request)

    all_mods = {i: get_mod_name(i) for i in get_downloaded_mods()}

    modset_.active_mods = [m.mod_steam_id for m in Arma3ModsetMod.where({'modset_id': modset_.id})]
    modset_.active_uninstalled_mods = {k: get_mod_name(k) for k in modset_.active_mods if k not in all_mods}

    return html(template.render(modset=modset_, all_mods=all_mods))


async def modset_post(request, modset_id):
    modset_ = Arma3Modset.find(modset_id)
    if modset_ is None:
        return response_404(request)

    args = request.form
    action = args.get('action', None)
    if action == 'update':
        all_mods = get_downloaded_mods()
        modset_.active_mods = [m.mod_steam_id for m in Arma3ModsetMod.where({'modset_id': modset_.id})]
        uninstalled_mods = [m for m in modset_.active_mods if m not in all_mods]
        all_mods.extend(uninstalled_mods)

        active_mods = [m.mod_steam_id for m in Arma3ModsetMod.where({'modset_id': modset_.id})]

        for mod_id in all_mods:
            active = args.get(f'mod_{mod_id}', False)
            if mod_id in active_mods and not active:
                mms = Arma3ModsetMod.where({'modset_id': modset_.id, 'mod_steam_id': mod_id})
                for mm in mms:
                    mm.delete()
            if mod_id not in active_mods and active:
                mm = Arma3ModsetMod()
                mm.modset_id = modset_id
                mm.mod_steam_id = mod_id
                mm.save()
    elif action == 'delete':
        modset_.delete()
        return redirect('/modsets')

    return redirect(f'/modsets/{modset_id}')
