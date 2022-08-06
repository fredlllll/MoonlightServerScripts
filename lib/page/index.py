from lib.apis.arma_3_server import get_server_controller, start_server, stop_server, restart_server, enable_server, disable_server
import logging
from sanic.response import html, redirect
from lib.jinja_templates import get_template
from lib.db.models.arma_3_server import Arma3Server
from lib.responses import response_404

logger = logging.getLogger(__name__)


async def index(request):
    servers = Arma3Server.all()
    statuses = []
    logs = []
    for server in servers:
        cont = get_server_controller(server.id)
        statuses.append(cont.get_state())
        logs.append(cont.get_log(100))

    template = get_template("index.html", request)
    return html(template.render(statuses=statuses, logs=logs, servers=servers))


async def index_post(request):
    args = request.form
    server_id = args.get('server-id', None)
    if server_id is None:
        return redirect('/')
    server = Arma3Server.find(server_id)
    if server is None:
        return response_404(request)
    if args.get('start', None) is not None:
        start_server(server)
    elif args.get('stop', None) is not None:
        stop_server(server)
    elif args.get('restart', None) is not None:
        restart_server(server)
    elif args.get('enable', None) is not None:
        enable_server(server)
    elif args.get('disable', None) is not None:
        disable_server(server)
    return redirect('/')
