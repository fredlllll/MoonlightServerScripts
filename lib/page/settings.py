import logging
from sanic.response import html, redirect
from lib.jinja_templates import get_template
from lib.responses import response_403
from lib.job_system.jobs.login_steamcmd_job import LoginSteamCmdJob
from lib.job_system.job_executer import JobExecuter

logger = logging.getLogger(__name__)


async def settings(request):
    if not request.ctx.has_permission('admin'):
        return response_403(request)
    template = get_template("settings.html", request)
    return html(template.render())


async def post_login_steamcli(request):
    user = request.form.get('user', None)
    password = request.form.get('password', None)
    auth_code = request.form.get('auth_code', None)

    job = LoginSteamCmdJob(user, password, auth_code)
    JobExecuter.add_job(job)

    return redirect('/jobs')


async def settings_post(request):
    action = request.form.get('action', None)

    response = None

    if action == 'login_steamcli':
        response = await post_login_steamcli(request)

    if response is None:
        response = redirect('/settings')
    return response
