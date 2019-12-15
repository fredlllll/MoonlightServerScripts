from Handlers.BaseHandler import BaseHandler
from tornado.web import authenticated
from APIs.SteamAPI import get_downloaded_mods, get_mod_name
from Handlers.Pages.Page_JobsHandler import Page_JobsHandler
from JobSystem.JobExecuter import JobExecuter
from JobSystem.Jobs.LinkModsJob import LinkModsJob
import logging

logger = logging.getLogger(__name__)


class Page_ModLinkerHandler(BaseHandler):
    """
    renders the page_index.html template
    """
    url_pattern = r'/mod_linker'
    url = '/mod_linker'

    def _get_mod_infos(self):
        mod_ids = get_downloaded_mods()

        mod_infos = []
        for mod_id in mod_ids:
            mod_infos.append({
                'id': mod_id,
                'name': get_mod_name(mod_id)
            })
        return mod_infos

    @authenticated
    def get(self, *args, **kwargs):
        mod_infos = self._get_mod_infos()

        self.render("page_mod_linker.html", mod_infos=mod_infos)

    @authenticated
    def post(self):
        mod_infos = self._get_mod_infos()
        checked_mod_ids = []

        for info in mod_infos:
            if self.get_argument('chk_' + info['id'], None) is not None:
                checked_mod_ids.append(info['id'])

        job = LinkModsJob(checked_mod_ids)
        JobExecuter.add_job(job)

        self.redirect(Page_JobsHandler.url)
