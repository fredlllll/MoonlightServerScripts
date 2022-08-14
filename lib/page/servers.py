import logging
from sanic.response import html
from lib.jinja_templates import get_template
from lib.db.models.arma_3_server import Arma3Server
from lib.db.models.arma_3_modset import Arma3Modset
from lib.apis.steam import update_server
from threading import Thread

logger = logging.getLogger(__name__)

update_thread: Thread = None


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
    return html(template.render(servers=servers_, update_thread=update_thread))


async def servers_post(request):
    global update_thread
    args = request.form
    if args.get('update-server', None) is not None and (update_thread is None or not update_thread.is_alive()):
        user = request.form.get('user', '')
        password = request.form.get('password', '')
        auth_code = request.form.get('auth_code', '')

        # TODO put this in job
        def do_it():
            update_server(user, password, auth_code)

        update_thread = Thread(target=do_it, daemon=True)
        update_thread.start()
