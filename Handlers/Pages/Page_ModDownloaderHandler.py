from Handlers.BaseHandler import BaseHandler
from Handlers.Pages.Page_JobsHandler import Page_JobsHandler
from tornado.web import authenticated
from APIs.SteamAPI import get_downloaded_mods, get_mod_name, get_collection_mod_ids
import logging
from JobSystem.Jobs.DownloadModsJob import DownloadModsJob
from JobSystem.Jobs.DeleteModsJob import DeleteModsJob
from JobSystem.JobExecuter import JobExecuter

logger = logging.getLogger(__name__)


class Page_ModDownloaderHandler(BaseHandler):
    """
    renders the page_index.html template
    """
    url_pattern = r'/mod_downloader'
    url = '/mod_downloader'

    @authenticated
    def get(self, *args, **kwargs):
        mod_ids = get_downloaded_mods()
        mod_infos = []
        for mod_id in mod_ids:
            mod_infos.append({
                'id': mod_id,
                'name': get_mod_name(mod_id)
            })

        self.render("page_mod_downloader.html", mod_infos=mod_infos)

    def post_download(self):
        collection_id = self.get_argument('collection_id', '')
        mod_ids_str = self.get_argument('mod_ids', '')
        if len(collection_id) > 0:
            mod_ids = get_collection_mod_ids(collection_id)
        elif len(mod_ids_str) > 0:
            mod_ids = mod_ids_str.split(',')
        else:
            self.redirect(self.url)  # TODO: note whats wrong
            return

        user = self.get_argument('user', '')
        password = self.get_argument('password', '')
        auth_code = self.get_argument('auth_code', '')

        job = DownloadModsJob(mod_ids, user, password, auth_code)
        JobExecuter.add_job(job)

        self.redirect(Page_JobsHandler.url)

    def post_delete(self):
        mod_id = self.get_argument('mod_id', None)
        if mod_id is None:
            self.redirect(self.url)
            return

        job = DeleteModsJob([mod_id])
        JobExecuter.add_job(job)

        self.redirect(Page_JobsHandler.url)
        
    def post_delete_all(self):
        mod_ids = get_downloaded_mods()
        job = DeleteModsJob(mod_ids)
        JobExecuter.add_job(job)

        self.redirect(Page_JobsHandler.url)

    @authenticated
    def post(self):
        action = self.get_argument('action', None)
        if action == 'download':
            self.post_download()
        elif action == 'delete':
            self.post_delete()
        elif action == 'delete-all':
            self.post_delete_all()
        else:
            self.redirect(self.url)
