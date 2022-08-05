import logging
from sanic.response import html
from lib.jinja_templates import get_template
from lib.db.models.arma_3_server import Arma3Server
from lib.db.models.arma_3_modset import Arma3Modset

logger = logging.getLogger(__name__)


async def servers(request):
    servers_ = Arma3Server.all()

    for s in servers_:
        if s.modset_id:
            try:
                s.modset = Arma3Modset.find(s.modset_id).name
            except:
                s.modset = 'Not Found'
        else:
            s.modset = 'None'

    template = get_template("servers.html", request)
    return html(template.render(servers=servers_))

async def servers_post(request):
    pass