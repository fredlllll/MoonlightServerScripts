from Handlers.BaseHandler import BaseHandler
import logging

logger = logging.getLogger(__name__)


class Page_403(BaseHandler):
    url_pattern = r'/403'
    url = '/403'

    def get(self, *args, **kwargs):
        self.set_status(403, "Access Denied")
        self.render("403.html")
