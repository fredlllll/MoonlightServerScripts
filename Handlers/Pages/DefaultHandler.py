from Handlers.BaseHandler import BaseHandler
import logging

logger = logging.getLogger(__name__)


class DefaultHandler(BaseHandler):
    """
    redirects to 404 for every action
    """

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
