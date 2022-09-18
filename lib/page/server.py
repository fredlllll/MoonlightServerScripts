import logging
from sanic.response import html, redirect
from lib.jinja_templates import get_template
from lib.db.models.arma_3_server import Arma3Server
from lib.db.models.arma_3_modset import Arma3Modset
from lib.responses import response_404
from lib.settings import Settings
from lib.arma_3_server_util import get_basic_config_content, set_basic_config_content, get_server_config_content, set_server_config_content, get_server_profile_content, set_server_profile_content
from lib.arma_3_server_util import get_basic_config_file_name, get_server_config_file_name, get_server_profile_file_name
from lib.apis.arma_3_server import get_server_controller, start_server, stop_server, restart_server, enable_server, disable_server
from lib.util import copy
from lib.constants import CREATORDLCS

logger = logging.getLogger(__name__)


async def server(request, server_id):
    server_ = Arma3Server.find(server_id)
    if server_ is None:
        return response_404(request)
    template = get_template("server.html", request)

    basic_config_content = get_basic_config_content(server_id)
    server_config_content = get_server_config_content(server_id)
    server_profile_content = get_server_profile_content(server_id)

    cont = get_server_controller(server_id)

    status = cont.get_state()
    log = cont.get_log(100)

    modsets = Arma3Modset.all()

    return html(template.render(server=server_, basic_config_content=basic_config_content, server_config_content=server_config_content, server_profile_content=server_profile_content, status=status, log=log, modsets=modsets, cdlcs=CREATORDLCS))


async def server_post(request, server_id):
    args = request.form

    server_ = Arma3Server.find(server_id)
    if server_ is None:
        return response_404(request)

    action = args.get('action', None)
    if action == 'set-modset':
        modset_id = args.get('modset', None)
        server_.modset_id = modset_id
        server_.save()
    elif action == 'set-port':
        try:
            port = int(args.get('port', 2302))
            server_.port = port
            server_.save()
        except ValueError:
            pass
    elif action == 'set-cdlcs':
        dlcs = []
        for abbrv, cdlc in CREATORDLCS.items():
            if args.get(f'cdlc-{abbrv}', None) is not None:
                dlcs.append(abbrv)
        server_.creator_dlcs = dlcs
        server_.save()
    elif action == 'update-basic-config':
        content = args.get('content')
        set_basic_config_content(server_id, content)
    elif action == 'update-server-config':
        content = args.get('content')
        set_server_config_content(server_id, content)
    elif action == 'update-server-profile':
        content = args.get('content')
        set_server_profile_content(server_id, content)
    elif action == 'reset-basic-config':
        copy("arma_server_default_files/basic.cfg", get_basic_config_file_name(server_id), Settings.local_steam_user, Settings.local_steam_user)
    elif action == 'reset-server-config':
        copy("arma_server_default_files/server.cfg", get_server_config_file_name(server_id), Settings.local_steam_user, Settings.local_steam_user)
    elif action == 'reset-server-profile':
        copy("arma_server_default_files/server.arma3profile", get_server_profile_file_name(server_id), Settings.local_steam_user, Settings.local_steam_user)
    elif action == 'state-change':
        if args.get('start', None) is not None:
            start_server(server_)
        elif args.get('stop', None) is not None:
            stop_server(server_)
        elif args.get('restart', None) is not None:
            restart_server(server_)
        elif args.get('enable', None) is not None:
            enable_server(server_)
        elif args.get('disable', None) is not None:
            disable_server(server_)
    elif action == 'delete':
        server_.delete()
        return redirect('/servers')

    return redirect(f'/servers/{server_id}')
