import logging
from sanic.response import html, redirect
from lib.jinja_templates import get_template
from lib.db.models.arma_3_server import Arma3Server
from lib.db.models.arma_3_modset import Arma3Modset
from lib.job_system.jobs.update_server_job import UpdateServerJob
from lib.job_system.job_executer import JobExecuter
from lib.constants import CREATORDLCS

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
    return html(template.render(servers=servers_, cdlcs=CREATORDLCS))


async def servers_post(request):
    args = request.form
    job = None
    if args.get('update-server', None) is not None:
        job = UpdateServerJob()
    if args.get('update-server-creator-dlc', None) is not None:
        job = UpdateServerJob('creatordlc')
    if job is not None:
        JobExecuter.add_job(job)
        return redirect('/jobs')

    return redirect('/servers')
