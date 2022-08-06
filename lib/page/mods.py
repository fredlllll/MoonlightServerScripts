from lib.apis.steam import get_downloaded_mods, get_mod_name, get_collection_mod_ids, delete_downloaded_mods
from lib.jinja_templates import get_template
from sanic.response import html, redirect
from lib.job_system.jobs.download_mods_job import DownloadModsJob
from lib.job_system.job_executer import JobExecuter
import logging

logger = logging.getLogger(__name__)


async def mods(request):
    mod_ids = get_downloaded_mods()
    mod_infos = []
    for mod_id in mod_ids:
        mod_infos.append({
            'id': mod_id,
            'name': get_mod_name(mod_id)
        })

    template = get_template('mods.html', request)
    return html(template.render(mod_infos=mod_infos))


async def post_download(request):
    collection_id = request.form.get('collection_id', '')
    mod_ids_str = request.form.get('mod_ids', '')
    if len(collection_id) > 0:
        mod_ids = get_collection_mod_ids(collection_id)
    elif len(mod_ids_str) > 0:
        mod_ids = mod_ids_str.split(',')
    else:
        return  # TODO: error message?

    user = request.form.get('user', '')
    password = request.form.get('password', '')
    auth_code = request.form.get('auth_code', '')

    job = DownloadModsJob(mod_ids, user, password, auth_code)
    JobExecuter.add_job(job)

    return redirect('/jobs')


async def post_delete(request):
    mod_id = request.form.get('mod_id', None)
    if mod_id is None:
        return

    delete_downloaded_mods([str(mod_id)])


async def post_delete_all(request):
    mod_ids = get_downloaded_mods()
    delete_downloaded_mods(mod_ids)


async def mods_post(request):
    action = request.form.get('action', None)

    response = None

    if action == 'download':
        response = await post_download(request)
    elif action == 'delete':
        response = await post_delete(request)
    elif action == 'delete-all':
        response = await post_delete_all(request)

    if response is None:
        response = redirect('/mod_downloader')
    return response
