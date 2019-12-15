from Handlers.BaseHandler import BaseHandler
from tornado.web import authenticated
from APIs.Arma3ServerAPI import Arma3ServerController
import logging

logger = logging.getLogger(__name__)


class Page_IndexHandler(BaseHandler):
    """
    renders the page_index.html template
    """
    url_pattern = r'/'
    url = '/'

    @authenticated
    def get(self, *args, **kwargs):
        status = Arma3ServerController.get_state()

        log = Arma3ServerController.get_log(100)

        self.render("page_index.html", status=status, log=log)

    @authenticated
    def post(self):
        if self.get_argument('start', None) is not None:
            Arma3ServerController.start()
        elif self.get_argument('stop', None) is not None:
            Arma3ServerController.stop()
        elif self.get_argument('restart', None) is not None:
            Arma3ServerController.restart()
        elif self.get_argument('enable', None) is not None:
            Arma3ServerController.enable()
        elif self.get_argument('disable', None) is not None:
            Arma3ServerController.disable()
        self.redirect(self.url)
