import logging
from sanic.response import html
from lib.jinja_templates import get_template
from lib.db.models.arma_3_server import Arma3Server

logger = logging.getLogger(__name__)


async def servers(request):
    servers_ = Arma3Server.all()

    return html(template.render(servers=servers_))    template = get_template("servers.html", request)