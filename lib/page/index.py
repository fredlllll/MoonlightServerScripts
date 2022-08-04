from lib.apis.arma_3_server import get_server_controller
import logging
from sanic.response import html, redirect
from lib.jinja_templates import get_template
from lib.db.models.arma_3_server import Arma3Server

logger = logging.getLogger(__name__)


async def index(request):
    servers = Arma3Server.all()
    statuses = []
    logs = []
    for server in servers:
        cont = get_server_controller(server.id)
        statuses.append(cont.get_state())
        logs.append(cont.get_log(100))

    template = await get_template("index.html", request)
    return html(template.render(statuses=statuses, logs=logs, servers=servers))


async def index_post(request):
    args = request.form
    server_id = args.get('server-id', None)
    if server_id is None:
        return redirect('/')
    cont = get_server_controller(server_id)
    if args.get('start', None) is not None:
        cont.start()
    elif args.get('stop', None) is not None:
        cont.stop()
    elif args.get('restart', None) is not None:
        cont.restart()
    elif args.get('enable', None) is not None:
        cont.enable()
    elif args.get('disable', None) is not None:
        cont.disable()
    return redirect('/')
