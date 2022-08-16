import logging
from sanic.response import html, redirect
from lib.jinja_templates import get_template
from lib.db.models.arma_3_server import Arma3Server
from lib.db.models.arma_3_modset import Arma3Modset
from threading import Thread
from lib.job_system.jobs.update_server_job import UpdateServerJob
from lib.job_system.job_executer import JobExecuter

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

        job = UpdateServerJob(user, password, auth_code)
        JobExecuter.add_job(job)

    return redirect('/servers')
