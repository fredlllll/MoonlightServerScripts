import logging
from sanic.response import html, redirect
from lib.jinja_templates import get_template
from lib.db.models.arma_3_server import Arma3Server
from lib.db.models.arma_3_modset import Arma3Modset
from lib.responses import response_404
from lib.settings import Settings
from lib.arma_3_server_util import get_basic_config_file_name, get_server_config_file_name, get_server_profile_file_name
from lib.apis.arma_3_server import get_server_controller, start_server, stop_server, restart_server, enable_server, disable_server
from lib.util import copy

logger = logging.getLogger(__name__)


async def server(request, server_id):
    server_ = Arma3Server.find(server_id)
    if server_ is None:
        return response_404(request)
    template = get_template("server.html", request)

    with open(get_basic_config_file_name(server_id), 'rb') as f:
        basic_config_content = f.read().decode()
    with open(get_server_config_file_name(server_id), 'rb') as f:
        server_config_content = f.read().decode()
    with open(get_server_profile_file_name(server_id), 'rb') as f:
        server_profile_content = f.read().decode()

    cont = get_server_controller(server_id)

    status = cont.get_state()
    log = cont.get_log(100)

    modsets = Arma3Modset.all()

    return html(template.render(server=server_, basic_config_content=basic_config_content, server_config_content=server_config_content, server_profile_content=server_profile_content, status=status, log=log, modsets=modsets))


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
    elif action == 'update-basic-config':
        content = args.get('content')
        with open(get_basic_config_file_name(server_id), 'wb') as f:
            f.write(content.encode())
    elif action == 'update-server-config':
        content = args.get('content')
        with open(get_server_config_file_name(server_id), 'wb') as f:
            f.write(content.encode())
    elif action == 'update-server-profile':
        content = args.get('content')
        with open(get_server_profile_file_name(server_id), 'wb') as f:
            f.write(content.encode())
    elif action == 'reset-basic-config':
        copy("arma_server_default_files/basic.cfg", get_basic_config_file_name(server_id), Settings.arma_3_server_user, Settings.arma_3_server_user)
    elif action == 'reset-server-config':
        copy("arma_server_default_files/server.cfg", get_server_config_file_name(server_id), Settings.arma_3_server_user, Settings.arma_3_server_user)
    elif action == 'reset-server-profile':
        copy("arma_server_default_files/server.arma3profile", get_server_profile_file_name(server_id), Settings.arma_3_server_user, Settings.arma_3_server_user)
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
