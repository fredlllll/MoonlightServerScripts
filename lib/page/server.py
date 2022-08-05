import logging
from sanic.response import html, redirect
from lib.jinja_templates import get_template
from lib.db.models.arma_3_server import Arma3Server
from lib.db.models.arma_3_modset import Arma3Modset
from lib.responses import response_404
from lib.arma_3_server_util import get_basic_config_file_name, get_server_config_file_name, get_server_profile_file_name
from lib.apis.arma_3_server import get_server_controller
from lib.util import copy

logger = logging.getLogger(__name__)


async def server(request, server_id):
    server_ = Arma3Server.find(server_id)
    if server_ is None:
        return response_404(request)
    template = get_template("server.html", request)

    with open(get_basic_config_file_name(server_id), 'r') as f:
        basic_config_content = f.read()
    with open(get_server_config_file_name(server_id), 'r') as f:
        server_config_content = f.read()
    with open(get_server_profile_file_name(server_id), 'r') as f:
        server_profile_content = f.read()

    cont = get_server_controller(server_id)

    state = cont.get_state()
    log = cont.get_log(100)

    modsets = Arma3Modset.all()

    return html(template.render(server=server_, basic_config_content=basic_config_content, server_config_content=server_config_content, server_profile_content=server_profile_content, state=state, log=log, modsets=modsets))


async def server_post(request, server_id):
    args = request.form

    server_ = Arma3Server.find(server_id)
    if server_ is None:
        return response_404(request)

    action = args.get('action', None)
    if action == 'set_modset':
        modset_id = args['modset']
        server_.modset_id = modset_id
        server_.save()
    elif action == 'update_basic_config':
        pass
    elif action == 'update_server_config':
        pass
    elif action == 'update_server_profile':
        pass
    elif action == 'reset_basic_config':
        copy("arma_server_default_files/basic.cfg", get_basic_config_file_name(server_id))
    elif action == 'reset_server_config':
        copy("arma_server_default_files/server.cfg", get_server_config_file_name(server_id))
    elif action == 'reset_server_profile':
        copy("arma_server_default_files/server.arma3profile", get_server_profile_file_name(server_id))
    return redirect(f'/server/{server_id}')
