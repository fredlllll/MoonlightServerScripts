import logging
from lib.util import copy
from sanic.response import html, redirect
from lib.jinja_templates import get_template
from lib.db.models.arma_3_server import Arma3Server
from lib.settings import Settings
from lib.apis.arma_3_server import create_service, create_startup_script
from lib.arma_3_server_util import get_basic_config_file_name, get_server_config_file_name, get_server_profile_file_name

logger = logging.getLogger(__name__)


async def new_server(request):
    template = get_template("new_server.html", request)
    return html(template.render())


async def new_server_post(request):
    args = request.form
    name = args.get('name', None)
    port = args.get('port', None)
    if name is None or port is None:
        return redirect('/new_server?error=Name or port missing')

    if len(name) < 3:
        return redirect('/new_server?error=Name too short')
    port = int(port)

    server = Arma3Server()
    server.name = name
    server.port = port
    server.save()

    # create files
    create_service(server)
    create_startup_script(server)
    copy("arma_server_default_files/basic.cfg", get_basic_config_file_name(server.id),  Settings.local_steam_user,  Settings.local_steam_user)
    copy("arma_server_default_files/server.cfg", get_server_config_file_name(server.id),  Settings.local_steam_user,  Settings.local_steam_user)
    copy("arma_server_default_files/server.arma3profile", get_server_profile_file_name(server.id),  Settings.local_steam_user,  Settings.local_steam_user)

    return redirect(f'/servers/{server.id}')
