import logging
from sanic.response import html
from lib.jinja_templates import get_template
from lib.db.models.arma_3_server import Arma3Server

logger = logging.getLogger(__name__)


async def add_server(request):
    template = await get_template("add_server.html", request)
    return html(template.render())


async def add_server_post(request):
    pass  # TODO
