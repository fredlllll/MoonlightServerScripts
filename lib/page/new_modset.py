import logging
from sanic.response import html, redirect
from lib.jinja_templates import get_template
from lib.db.models.arma_3_modset import Arma3Modset

logger = logging.getLogger(__name__)


async def new_modset(request):
    template = get_template("new_modset.html", request)
    return html(template.render())


async def new_modset_post(request):
    args = request.form
    name = args.get('name', None)
    if name is None:
        return redirect('/new_modset?error=Name missing')

    if len(name) < 3:
        return redirect('/new_modset?error=Name too short')

    modset = Arma3Modset()
    modset.name = name
    modset.save()

    return redirect(f'/modsets/{modset.id}')
