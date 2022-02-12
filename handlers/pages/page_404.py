from handlers.MoonlightBaseHandler import MoonlightBaseHandler
import logging

logger = logging.getLogger(__name__)


class Page404(MoonlightBaseHandler):
    url = '/404'

    def get(self, *args, **kwargs):
        self.set_status(404, "Not Found")
        self.render("404.html")
