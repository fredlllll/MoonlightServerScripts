from Handlers.MoonlightBaseHandler import MoonlightBaseHandler
import logging

logger = logging.getLogger(__name__)


class Page403(MoonlightBaseHandler):
    url = '/403'

    def get(self, *args, **kwargs):
        self.set_status(403, "Access Denied")
        self.render("403.html")
