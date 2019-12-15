from Handlers.BaseHandler import BaseHandler
from tornado.web import authenticated
import logging
from Models.JobInfo import JobInfo, WAITING, EXECUTING

logger = logging.getLogger(__name__)


class Page_JobsHandler(BaseHandler):
    """
    renders the page_index.html template
    """
    url_pattern = '/jobs'
    url = '/jobs'

    @authenticated
    def get(self, *args, **kwargs):
        jobs = JobInfo.all()
        job_infos = []
        for job in jobs:
            job_infos.append({
                'name': job.name,
                'info': job.info,
                'status': job.status,
                'error': job.error
            })

        self.render("page_jobs.html", job_infos=job_infos)

    @authenticated
    def post(self):
        if self.get_argument('clear_jobs', None) is not None:
            jobs = JobInfo.delete_where({'$and': [{
                'status': {
                    '$ne': WAITING
                }
            }, {
                'status': {
                    '$ne': EXECUTING
                }
            }]})
        self.redirect(self.url)
