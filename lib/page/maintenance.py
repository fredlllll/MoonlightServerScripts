import logging
import os

from sanic.response import html, redirect
from lib.jinja_templates import get_template
from lib.responses import response_403
from lib.apis.steam import get_arma_workshop_acf_path

logger = logging.getLogger(__name__)


async def maintenance(request):
    if not request.ctx.has_permission('admin'):
        return response_403(request)
    template = get_template("maintenance.html", request)
    return html(template.render())


async def maintenance_post(request):
    if request.form.get('delete-mods-acf', None) is not None:
        os.unlink(get_arma_workshop_acf_path())

    return redirect('/maintenance')
