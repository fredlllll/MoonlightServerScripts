from Handlers.BaseHandler import BaseHandler
from tornado.web import  authenticated
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
        self.render("page_index.html")
