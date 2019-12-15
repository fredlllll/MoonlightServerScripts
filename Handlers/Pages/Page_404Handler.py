from Handlers.BaseHandler import BaseHandler
import logging

logger = logging.getLogger(__name__)


class Page_404(BaseHandler):
    url_pattern = r'/404'
    url = '/404'

    def get(self, *args, **kwargs):
        self.set_status(404, "Not Found")
        self.render("404.html")
