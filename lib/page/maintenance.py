import logging
from sanic.response import html, redirect
from lib.jinja_templates import get_template
from lib.responses import response_403
from lib.job_system.jobs.login_steamcmd_job import LoginSteamCmdJob
from lib.job_system.job_executer import JobExecuter

logger = logging.getLogger(__name__)


async def maintenance(request):
    if not request.ctx.has_permission('admin'):
        return response_403(request)
    template = get_template("maintenance.html", request)
    return html(template.render())


async def maintenance_post(request):
    if request.form.get('delete-mods-acf', None) is not None:
        pass

    return redirect('/maintenance')
