from lib.apis.arma_3_server import Arma3ServerController
import logging
from sanic.response import html, redirect
from lib.jinja_templates import get_template

logger = logging.getLogger(__name__)


async def index(request):
    status = Arma3ServerController.get_state()

    log = Arma3ServerController.get_log(100)

    template = await get_template("index.html", request)
    return html(template.render(status=status, log=log))


async def index_post(request):
    args = request.form
    if args.get('start', None) is not None:
        Arma3ServerController.start()
    elif args.get('stop', None) is not None:
        Arma3ServerController.stop()
    elif args.get('restart', None) is not None:
        Arma3ServerController.restart()
    elif args.get('enable', None) is not None:
        Arma3ServerController.enable()
    elif args.get('disable', None) is not None:
        Arma3ServerController.disable()
    return redirect('/')
