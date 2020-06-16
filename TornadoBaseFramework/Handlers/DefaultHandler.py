from tornado.web import RequestHandler
import logging

logger = logging.getLogger(__name__)


class DefaultHandler(RequestHandler):
    """
    redirects to 404 for every action
    """

    def redirect_404(self):
        self.redirect('/404')

    def head(self, *args, **kwargs):
        self.redirect_404()

    def get(self, *args, **kwargs):
        self.redirect_404()

    def post(self, *args, **kwargs):
        self.redirect_404()

    def delete(self, *args, **kwargs):
        self.redirect_404()

    def patch(self, *args, **kwargs):
        self.redirect_404()

    def put(self, *args, **kwargs):
        self.redirect_404()

    def options(self, *args, **kwargs):
        self.redirect_404()
