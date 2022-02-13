import logging
from sanic.response import html
from lib.jinja_templates import get_template
from lib.db.models.arma_3_server import Arma3Server

logger = logging.getLogger(__name__)


async def servers(request):
    servers = await Arma3Server.all()

    template = await get_template("servers.html", request)
    return html(template.render(servers=servers))